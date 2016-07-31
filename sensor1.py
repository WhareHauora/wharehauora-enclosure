import solid as s
import solid.utils as u
import math

# basic dimensions
width = 83.0
height = 30.0
depth = 75.0
wall_width = 2.5
nt = 0.45  # nestle tolerance, so body and lid fit together
emboss_depth = 0.5  # logo emboss depth

# board guide dimensions
boards_height_inner = 10.5  # top of Uno to bottm of shield
board_width = 54.0
guide_z = 8.0
guide1_y = 2.5
guide2_y = 50.8
guide_depth = 8.0
guide_width = 3.0
lid_guide_bot_z = 6.0
lid_guide_top_z = 20.0
lid_guide_width = 8.0
lid_guide_y = 0.0
lid_guide_padding = 2.0  # pushes the board against the body

# dimensions for M3 25mm bolts
bolt_hole_clear = 3.0
bolt_hole_tapped = 2.5  # self-tapping into plastic
bolt_head_dia = 6.0  # 5 plus clearance
bolt_from_edge = 4.0
bolt_base_dia = 7.0

# dimensions for holes
power_y, power_z = 45.8, 14.5
power_width = 12.0
power_height = 12.0
usb_y, usb_z = 14.3, 10.0
usb_width = 12.0
usb_height = 9.0
sensor_x, sensor_y = 56.1, 27.0
sensor_width = 18.0
sensor_depth = 26.0

# misc
segments = 128
logo_file = 'logo_whare.dxf'

# derived dimensions
walls_width = wall_width * 2.0
half_wall_width = wall_width / 2.0
outer_rad = height / 2.0
inner_rad = outer_rad - wall_width
inner_height = height - walls_width
inner_depth = depth - walls_width
# lid depth goes as far as the end of the sensor hole
top_hole_depth = depth - sensor_x + (sensor_depth / 2.0)
half_guide_width = guide_width / 2.0

square_width = width - height  # the width without the round edge
bolt_z = height / 2.0
bolt1_y = bolt_from_edge - outer_rad
bolt2_y = square_width + outer_rad - bolt_from_edge
bolt_base1_y = (bolt_base_dia / 2.0) - outer_rad
bolt_base2_y = square_width + outer_rad - (bolt_base_dia / 2.0)
bolt_base_depth = depth * 0.66
# rotation of bolt base to merge into the side
bolt_base_angle = math.degrees(math.atan2(
    bolt_base_depth, bolt_base_dia / 2.0))
hnt = nt / 2.0  # half nested tolerance

# body centre
body = s.cube(size=[depth, square_width, height])
# body round edge 1
body += u.up(outer_rad)(s.rotate(a=[0, 90, 0])(
    s.cylinder(r=outer_rad, h=depth, segments=segments)
))
# body round edge 2
body += u.forward(square_width)(u.up(outer_rad)(s.rotate(a=[0, 90, 0])(
    s.cylinder(r=outer_rad, h=depth, segments=segments)
)))

# inner to subtract from the body for the body
inner = s.cube(
    size=[depth - wall_width, square_width, height - walls_width]
)
inner += u.up(inner_rad)(s.rotate(a=[0, 90, 0])(
    s.cylinder(r=inner_rad, h=depth - wall_width, segments=segments)
))
inner += u.forward(square_width)(u.up(inner_rad)(
    s.rotate(a=[0, 90, 0])(
        s.cylinder(r=inner_rad, h=depth - wall_width, segments=segments)
    )
))

# subtract inner from body
body -= u.right(wall_width)(u.up(wall_width)(inner))

# subtract sensor hole
body -= u.forward(sensor_y - sensor_width / 2.0)(
    u.right(depth - top_hole_depth + half_wall_width)(u.up(
        height - wall_width)(
            s.cube(size=[depth - top_hole_depth, sensor_width, wall_width])
    ))
)

# bolt base 1
body += u.up(bolt_z)(u.forward(bolt_base1_y)(u.right(depth - half_wall_width)(
    s.rotate(a=[90 - bolt_base_angle, -90, 0])(
        s.cylinder(
            d1=bolt_base_dia, d2=0.0, h=bolt_base_depth, segments=segments)
    )
)))
body -= u.up(bolt_z)(u.forward(bolt1_y)(u.right(depth)(
    s.rotate(a=[0, -90, 0])(
        s.cylinder(d=bolt_hole_tapped, h=bolt_base_depth, segments=segments)
    )
)))
# bolt base 2
body += u.up(bolt_z)(u.forward(bolt_base2_y)(u.right(depth - half_wall_width)(
    s.rotate(a=[bolt_base_angle - 90, -90, 0])(
        s.cylinder(
            d1=bolt_base_dia, d2=0.0, h=bolt_base_depth, segments=segments)
    )
)))
body -= u.up(bolt_z)(u.forward(bolt2_y)(u.right(depth)(
    s.rotate(a=[0, -90, 0])(
        s.cylinder(d=bolt_hole_tapped, h=bolt_base_depth, segments=segments)
    )
)))

# subtract lid side nestle
body -= u.up(half_wall_width)(u.right(depth - half_wall_width)(
    s.cube(size=[
        half_wall_width,
        square_width,
        height - wall_width
    ])
))
body -= u.right(depth - half_wall_width)(u.up(inner_rad + wall_width)(
    s.rotate(a=[0, 90, 0])(
        s.cylinder(r=inner_rad + half_wall_width, h=half_wall_width,
                   segments=segments)
    )
))
body -= u.forward(square_width)(u.right(depth - half_wall_width)(
    u.up(inner_rad + wall_width)(
        s.rotate(a=[0, 90, 0])(
            s.cylinder(r=inner_rad + half_wall_width, h=half_wall_width,
                       segments=segments)
        )
    )
))

# body guides
body += u.up(guide_z)(u.forward(guide1_y - wall_width - half_guide_width)(
    s.cube(size=[guide_depth, wall_width, boards_height_inner])
))
body += u.up(guide_z)(u.forward(guide1_y + half_guide_width)(
    s.cube(size=[guide_depth, wall_width, boards_height_inner])
))
body += u.up(guide_z)(u.forward(guide2_y - wall_width - half_guide_width)(
    s.cube(size=[guide_depth, wall_width, boards_height_inner])
))
body += u.up(guide_z)(u.forward(guide2_y + half_guide_width)(
    s.cube(size=[guide_depth, wall_width, boards_height_inner])
))


# lid side nestle
lid = u.up(half_wall_width + hnt)(u.right(depth + hnt - half_wall_width)(
    s.cube(size=[
        half_wall_width,
        square_width,
        height - wall_width - nt
    ])
))
lid += u.right(depth + hnt - half_wall_width)(u.up(inner_rad + wall_width)(
    s.rotate(a=[0, 90, 0])(
        s.cylinder(r=inner_rad + half_wall_width - hnt, h=half_wall_width,
                   segments=segments)
    )
))
lid += u.forward(square_width)(u.right(depth + hnt - half_wall_width)(
    u.up(inner_rad + wall_width)(
        s.rotate(a=[0, 90, 0])(
            s.cylinder(r=inner_rad + half_wall_width - hnt, h=half_wall_width,
                       segments=segments)
        )
    )
))

# lid side
lid += u.right(depth)(
    s.cube(size=[
        half_wall_width,
        square_width,
        height
    ])
)
lid += u.right(depth)(u.up(outer_rad)(
    s.rotate(a=[0, 90, 0])(
        s.cylinder(r=outer_rad, h=half_wall_width,
                   segments=segments)
    )
))
lid += u.forward(square_width)(u.right(depth)(u.up(outer_rad)(
    s.rotate(a=[0, 90, 0])(
        s.cylinder(r=outer_rad, h=half_wall_width,
                   segments=segments)
    )
)))

# lid holes
# power hole
lid -= u.up(power_z)(u.forward(power_y)(u.right(depth)(
    s.cube(size=[wall_width, power_width, power_height], center=True)
)))
# usb hole
lid -= u.up(usb_z)(u.forward(usb_y)(u.right(depth)(
    s.cube(size=[wall_width, usb_width, usb_height], center=True)
)))
# sensor hole
lid -= u.up(height)(u.forward(sensor_y)(u.right(sensor_x)(
    s.cube(size=[sensor_depth, sensor_width, walls_width], center=True)
)))
# bolt hole 1
lid -= u.up(bolt_z)(u.forward(bolt1_y)(u.right(depth + half_wall_width)(
    s.rotate(a=[0, -90, 0])(
        s.cylinder(d=bolt_hole_clear, h=wall_width, segments=segments)
    )
)))
# bolt hole 2
lid -= u.up(bolt_z)(u.forward(bolt2_y)(u.right(depth + half_wall_width)(
    s.rotate(a=[0, -90, 0])(
        s.cylinder(d=bolt_hole_clear, h=wall_width, segments=segments)
    )
)))

# lid guides
# lid guide top
lid += u.up(lid_guide_bot_z - wall_width)(u.forward(lid_guide_y)(
    u.right(depth - half_wall_width - guide_depth + hnt)(
        s.cube(size=[guide_depth, lid_guide_width, wall_width])
    )
))
# lid guide bottom
lid += u.up(lid_guide_top_z)(u.forward(lid_guide_y)(
    u.right(depth - half_wall_width - guide_depth + hnt)(
        s.cube(size=[guide_depth, lid_guide_width, wall_width])
    )
))
# lid guide usb side
lid += u.up(lid_guide_bot_z - wall_width)(u.forward(lid_guide_y - wall_width)(
    u.right(depth - half_wall_width - guide_depth + hnt)(
        s.cube(size=[guide_depth, wall_width,
                     lid_guide_top_z - lid_guide_bot_z + wall_width * 2])
    )
))
# lid guide power side
lid += u.up(lid_guide_bot_z - wall_width)(u.forward(lid_guide_y + board_width)(
    u.right(depth - half_wall_width - guide_depth + hnt)(
        s.cube(size=[guide_depth, wall_width,
                     lid_guide_top_z - lid_guide_bot_z + wall_width * 2])
    )
))
# lid guide padding top
lid += u.up(lid_guide_bot_z)(u.forward(lid_guide_y)(
    u.right(depth - half_wall_width - lid_guide_padding + hnt)(
        s.cube(size=[lid_guide_padding, lid_guide_width, wall_width])
    )
))
# lid guide padding bottom
lid += u.up(lid_guide_top_z - wall_width)(u.forward(lid_guide_y)(
    u.right(depth - half_wall_width - lid_guide_padding + hnt)(
        s.cube(size=[lid_guide_padding, lid_guide_width, wall_width])
    )
))
# lid guide padding bottom on power side
lid += u.up(lid_guide_bot_z)(
    u.forward(lid_guide_y + board_width - lid_guide_width)(
        u.right(depth - half_wall_width - lid_guide_padding + hnt)(
            s.cube(size=[lid_guide_padding, lid_guide_width, wall_width])
        )
    )
)

logo = u.right(40)(u.up(height - emboss_depth)(
    s.linear_extrude(height=emboss_depth)(
        s.rotate(a=[0, 0, 90])(
            s.import_(file=logo_file)
        )
    )
))

body -= logo


def render(suffix, final):
    suffix += '.scad'
    s.scad_render_to_file(final, __file__.replace('.py', suffix))

# rotate and split into 2 files for printing
render(
    '-print-body',
    s.rotate(a=[0, -90, 0])(body))
render(
    '-print-lid',
    s.rotate(a=[0, 90, 0])(lid)
)

# explode for viewing inside
render(
    '-explode',
    body + u.up(outer_rad * 3)(lid)
)

# final assembled shape
render(
    '',
    body + lid
)
