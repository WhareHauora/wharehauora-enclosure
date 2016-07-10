import solid as s
import solid.utils as u

# basic dimensions
width = 83.0
height = 30.0
depth = 75.0
wall_width = 2.5
nt = 0.45  # nestle tolerance, so body and lid fit together
emboss_depth = 0.5  # logo emboss depth

# bottom of the Uno board to the top of the shield
# taking no account of the components
board_height = 15.0
pins_height = 2.0  # height of component pins off the board

# dimensions for M3 25mm bolts
bolt_hole_clear = 3.0
bolt_hole_tapped = 2.5  # self-tapping into plastic
bolt_head_dia = 6.0  # 5 plus clearance
bolt_lid_height = 7.0  # underside of lid to top of shield board
bolt_dia1 = 10.0
bolt_dia2 = 5.0
bolt1_x, bolt1_y = 6.9, 45.7
bolt2_x, bolt2_y = 56.8, 2.5
bolt3_x, bolt3_y = 58.1, 50.8

# dimensions for holes
power_y, power_z = 45.8, 15.5
power_width = 12.0
power_height = 12.0
usb_y, usb_z = 14.3, 11.0
usb_width = 12.0
usb_height = 9.0
sensor_x, sensor_y = 56.1, 27.0
sensor_width = 18.0
sensor_depth = 24.0

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
bolt_body_height = inner_height - board_height - bolt_lid_height
# lid depth goes as far as the end of the sensor hole
lid_depth = depth - sensor_x + (sensor_depth / 2.0)

square_width = width - height  # the width without the round edge
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

# subtract lid top nestle
body -= u.right(depth - lid_depth + half_wall_width)(u.up(
    height - half_wall_width)(
        s.cube(size=[depth - lid_depth, square_width, half_wall_width])
))
body -= u.forward(half_wall_width)(u.right(depth - lid_depth + wall_width)(
    u.up(height - wall_width)(
        s.cube(size=[
            depth - lid_depth - wall_width,
            square_width - wall_width,
            half_wall_width
        ])
    )
))

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

# lid top
lid = u.forward(hnt)(u.right(depth - lid_depth + half_wall_width + hnt)(
    u.up(height - half_wall_width)(
        s.cube(size=[lid_depth - nt, square_width - nt, half_wall_width])
    )
))
lid += u.forward(half_wall_width + hnt)(u.right(
    depth - lid_depth + wall_width + hnt)(
        u.up(height - wall_width)(
            s.cube(size=[
                lid_depth - half_wall_width - nt,
                square_width - wall_width - nt,
                half_wall_width
            ])
        )
    )
)

# lid side nestle
lid += u.up(half_wall_width + hnt)(u.right(depth + hnt - half_wall_width)(
    s.cube(size=[
        half_wall_width,
        square_width,
        height - half_wall_width - nt
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

# lid bolt mount
bolt_lid = u.up(height - bolt_lid_height - wall_width)(
    s.cylinder(d1=bolt_dia2, d2=bolt_dia1, h=bolt_lid_height + wall_width,
               segments=segments) -
    s.cylinder(d=bolt_hole_tapped, h=bolt_lid_height + 1.0, segments=segments)
)
body += u.right(bolt1_x)(u.forward(bolt1_y)(bolt_lid))
lid += u.right(bolt2_x)(u.forward(bolt2_y)(bolt_lid))
lid += u.right(bolt3_x)(u.forward(bolt3_y)(bolt_lid))

# lid holes
power_hole = u.up(power_z)(u.forward(power_y)(u.right(depth)(
    s.cube(size=[wall_width, power_width, power_height], center=True)
)))
lid -= power_hole
usb_hole = u.up(usb_z)(u.forward(usb_y)(u.right(depth)(
    s.cube(size=[wall_width, usb_width, usb_height], center=True)
)))
lid -= usb_hole
sensor_hole = u.up(height)(u.forward(sensor_y)(u.right(sensor_x)(
    s.cube(size=[sensor_depth, sensor_width, walls_width], center=True)
)))
lid -= sensor_hole

# body subtraction for lid bolt mount
bolt_lid = u.up(height - bolt_lid_height - wall_width - nt)(
    s.cylinder(d1=bolt_dia2 + hnt, d2=bolt_dia1 + hnt,
               h=bolt_lid_height + wall_width + nt,
               segments=segments)
)
body -= u.right(bolt2_x)(u.forward(bolt2_y)(bolt_lid))
body -= u.right(bolt3_x)(u.forward(bolt3_y)(bolt_lid))

# body bolt mount
bolt_body = u.up(wall_width)(
    s.cylinder(d1=bolt_dia1, d2=bolt_dia2, h=bolt_body_height,
               segments=segments)
)
body += u.right(bolt1_x)(u.forward(bolt1_y)(bolt_body))
body += u.right(bolt2_x)(u.forward(bolt2_y)(bolt_body))
body += u.right(bolt3_x)(u.forward(bolt3_y)(bolt_body))

# bolt body hole
bolt_body_hole = (
    s.cylinder(d=bolt_head_dia, h=wall_width, segments=segments) +
    s.cylinder(d=bolt_hole_clear, h=wall_width + bolt_body_height,
               segments=segments)
)
body -= u.right(bolt1_x)(u.forward(bolt1_y)(bolt_body_hole))
body -= u.right(bolt2_x)(u.forward(bolt2_y)(bolt_body_hole))
body -= u.right(bolt3_x)(u.forward(bolt3_y)(bolt_body_hole))

# pins next to bolt 2
pins_hole = u.up(wall_width + bolt_body_height - pins_height)(
    u.forward(bolt2_y)(u.right(bolt2_x - 3.0)(
        s.cylinder(d=3, h=pins_height + board_height + pins_height)
    ))
)
body -= pins_hole
lid -= pins_hole

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
