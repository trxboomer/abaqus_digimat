from utils.data_parsing import line_to_list
import numpy as np


def get_dimensions(path: str):

    dimensions: list[np.float64] = []
    with open(f"{path}/Template.daf", "r") as f:
        for line in f:
            if "size_rve" in line:
                params = line_to_list(line, "=")
                dimensions.append(np.float64(params[1]))

    if len(dimensions) == 1:
        return np.full((3, 1), dimensions[0])

    if len(dimensions) == 3:
        return np.array(dimensions)

    else:
        raise Exception(
            f"RVE dimensions found in .daf file incorrect, number of dimensions should be 1 or 3 not {len(dimensions)}"
        )
