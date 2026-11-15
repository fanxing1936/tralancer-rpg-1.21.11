"""Raise the cyan shoulder caps on the M4 Prime Enchanter model."""

import argparse
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'm3'))
from author import read, sha, write


LIFT = Decimal('1.8')
BASELINE_SHA = 'f7c6643d7d5227c7a89bc36f7630c3a7d6ce34a968d4e9c117326e617c7fce34'
CAP_PANELS = {f'{side}_shoulder_{face}' for side in ('left', 'right')
              for face in ('north', 'south', 'east', 'west')}
CAP_CUBES = CAP_PANELS | {'left_shoulder_top', 'right_shoulder_top'}


def raise_shoulders(source, amount=LIFT):
    model = deepcopy(source)

    def lift(vector):
        vector[1] = float(Decimal(str(vector[1])) + amount)

    panels = [bone for bone in model['groups'] if bone['name'] in CAP_PANELS]
    caps = [cube for cube in model['elements'] if cube['name'] in CAP_CUBES]
    assert len(panels) == 8 and len(caps) == 10
    for bone in panels:
        lift(bone['origin'])
    for cube in caps:
        lift(cube['from'])
        lift(cube['to'])
        if any(cube.get('rotation', ())):
            lift(cube['origin'])
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('baseline_sockets', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('output_sockets', type=Path)
    parser.add_argument('--lift', type=Decimal, default=LIFT, help='Total local Y offset from the M4 model')
    args = parser.parse_args()
    assert sha(args.baseline) == BASELINE_SHA
    old_sockets = read(args.baseline_sockets)
    assert old_sockets['bbmodel_sha256'] == BASELINE_SHA
    model = raise_shoulders(read(args.baseline), args.lift)
    write(args.output, model)
    # Both fist bones and all other socket anchors keep their M4 transforms.
    old_sockets['bbmodel_sha256'] = sha(args.output)
    write(args.output_sockets, old_sockets)


if __name__ == '__main__':
    main()
