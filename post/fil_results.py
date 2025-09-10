from dataclasses import dataclass, fields
import re
from typing import Callable, Generator, List, Sequence, Type, Union, Optional
import numpy as np
import numpy.typing as npt
import os
import tqdm


@dataclass
class OutVars:
    def header(self):
        return [f.name for f in fields(self)]

    def output(self) -> list[np.float64] | np.ndarray:  # type: ignore
        pass


class vector(OutVars):
    def __init__(self, params: list[np.float64]):
        self.magnitude: np.float64 = params[0]
        self.x: np.float64 = params[1]
        self.y: np.float64 = params[2]
        self.z: np.float64 = params[3]

    def output(self):
        return [self.magnitude, self.x, self.y, self.z]


@dataclass
class hfl(OutVars):
    int1: Optional[vector] = None
    int2: Optional[vector] = None
    int3: Optional[vector] = None
    int4: Optional[vector] = None

    def output(self):
        data = [self.int1, self.int2, self.int3, self.int4]
        items: list[np.float64] = []
        for int_point in data:
            items.extend(int_point.output())

        return items


@dataclass
class evol(OutVars):
    volume: np.float64

    def output(self):
        return [self.volume]


@dataclass
class orientation(OutVars):
    orientation: np.ndarray

    def output(self):
        return self.orientation


record_type = List[Union[int, np.float64, str]]

element_data_type = dict[str, dict[int, OutVars]]


class fil_parser:
    def __init__(self, path: str, file_name: str, include: list[int]):
        self.file_path = f"{path}/{file_name}"
        self.iter_pattern = re.compile(r"(?<=\*)+.+?(?=\*)|(?<=\*)+.+?(?=$)")
        self.record_pattern = re.compile(r"(D[\s-]\d\.\d+D[+-]\d{2}|I\s\d+|A.{8})")
        self.record = self.open_fil()
        self.include = include
        self.element_data: element_data_type = {}
        self.initiate_dict()

    def parse_line(self, line: str):
        # Insert a delimiter before each type prefix unless it is at the line start
        tokens = self.record_pattern.split(line)
        result: record_type = []
        for token in tokens:
            if not token:
                continue
            type_char = token[0]
            value_str = token[1:]
            if type_char == "I":
                # May be multiple integers in one block
                result.append(int(value_str[2:]))
            elif type_char == "D":
                result.append(np.float64(value_str.replace("D", "E")))
            elif type_char == "A":
                result.append(value_str.strip())
        return result[1], result[2:]

    def open_fil(
        self,
    ) -> Generator[
        tuple[int, list[Union[int, str, np.float64]]]
    ]:  # fix string formatting (use {filename} not "filename")
        with open(self.file_path, "r") as result:
            content = result.read().replace("\n", "")

            # Your regex pattern

            # Use re.finditer to get an iterator of match objects
            for match in self.iter_pattern.finditer(content):
                yield self.parse_line(match.group())  # type: ignore

            del content

    def initiate_dict(self):
        for var in self.include:
            self.element_data[self.out_var_code[var].__name__] = {}

    def get_element_data(self):
        for line in self.record:
            if line[0] == 1911:
                break

        for line in self.record:
            if line[0] == 1:
                data_key = line[1][:2]

            if any(x == line[0] for x in self.include):

                self.parsing_map[line[0]](
                    self, element_num=data_key[0], int_num=data_key[1], params=line[1]
                )

    def parse_hfl(
        self, element_num: int, int_num: int, params: list[np.float64]
    ) -> None:
        if element_num not in self.element_data["hfl"]:
            self.element_data["hfl"][element_num] = hfl()
        setattr(self.element_data["hfl"][element_num], f"int{int_num}", vector(params))

    def parse_volume(
        self, element_num: int, int_num: int, params: list[np.float64]
    ) -> None:
        self.element_data["evol"][element_num] = evol(params[0])

    def parse_orientation(
        self, element_num: int, int_num: int, params: list[np.float64]
    ):
        self.element_data["orientation"][element_num] = orientation(np.array(params))

    parsing_map = {28: parse_hfl, 78: parse_volume, 85: parse_orientation}

    out_var_code: dict[int, Type[OutVars]] = {28: hfl, 78: evol, 85: orientation}


def get_transform_matrix(x: np.ndarray, y: np.ndarray):
    z = np.cross(x, y)

    return np.transpose(np.stack((x, y, z), axis=0))


def save_parsed_data(data: element_data_type, path: str, file_name: str):

    for var_name, var in data.items():
        items: list[list[Union[int, np.float64]]] = []
        for element_num, element in var.items():
            items.append([element_num, *element.output()])

        np.save(f"{path}/{file_name[:-4]}-{var_name}.npy", np.array(items))


def batched_parse_save(path: str):
    fil_files = [f for f in os.listdir(path) if f.endswith(".fil")]

    print(f"Found {len(fil_files)} files to parse")
    for filename in tqdm.tqdm(fil_files, desc="Parsing .fil files"):
        try:
            fil_parse = fil_parser(
                path=path,
                file_name=filename,
                include=[28, 78, 85],
            )

            fil_parse.get_element_data()
            save_parsed_data(fil_parse.element_data, path=path, file_name=filename)

        except Exception as e:
            print(e)
            print(filename)
