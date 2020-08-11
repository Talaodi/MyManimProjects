from manimlib.imports import *


class Differential(GraphScene):
    CONFIG = {
        "x_min": -6,
        "x_max": 6,
        "y_min": -10,
        "y_max": 10,
        "graph_origin": ORIGIN,
        "x_axis_width": 14,
        "y_axis_height": 7.6
    }

    def construct(self):
        self.setup_axes(animate=True)
        self.square_graph = self.get_graph(lambda x: x ** 2, color=RED)
        self.play(ShowCreation(self.square_graph))
        self.wait(2)

        start_point = Dot(self.input_to_graph_point(
            1, self.square_graph)).set_color(BLUE)
        end_point = Dot(self.input_to_graph_point(
            3, self.square_graph)).set_color(BLUE)
        start_line = Line(self.coords_to_point(
            1, 0), self.coords_to_point(1, 0)).set_color(YELLOW)
        end_line = Line(self.coords_to_point(3, 0),
                        self.coords_to_point(3, 0)).set_color(YELLOW)
        line = Line(start_point.get_center(), end_point.get_center())
        line.set_length(8)
        self.add(VGroup(start_line, end_line))

        self.play(
            ShowCreation(VGroup(start_point, end_point)),
            start_line.put_start_and_end_on, self.coords_to_point(
                1, 0), start_point.get_center(),
            end_line.put_start_and_end_on, self.coords_to_point(
                3, 0), end_point.get_center()
        )

        self.wait(1)
        self.play(Write(line))
        start_x = ValueTracker(1)
        end_x = ValueTracker(3)
        start_point.add_updater(
            lambda m: m.move_to(self.input_to_graph_point(
                start_x.get_value(), self.square_graph))
        )
        end_point.add_updater(
            lambda m: m.move_to(self.input_to_graph_point(
                end_x.get_value(), self.square_graph))
        )

        def line_move(mobject: Line):
            if np.all(start_point.get_center() == end_point.get_center()):
                return mobject

            mobject.put_start_and_end_on(
                start_point.get_center(), end_point.get_center())
            mobject.set_length(8)
            return mobject

        line.add_updater(line_move)
        self.wait(2)
        self.play(FadeOut(VGroup(start_line, end_line)))
        self.play(
            start_x.increment_value, 1,
            end_x.increment_value, -1,
            run_time=4
        )

        text_x_eq_2 = TexMobject("x=2").next_to(
            self.coords_to_point(2, 0), DOWN)
        text_slope = TextMobject("Slope =", "4").scale(
            1.25).next_to(text_x_eq_2, DOWN)
        text_2x = TexMobject("2x").scale(1.25).next_to(text_slope[0], RIGHT)
        mid_line = Line(self.coords_to_point(2, 4),
                        self.coords_to_point(2, 4)).set_color(YELLOW)

        self.play(
            Write(text_x_eq_2),
            mid_line.put_start_and_end_on, self.coords_to_point(
                2, 4), self.coords_to_point(2, 0)
        )
        self.play(Write(text_slope), run_time=2)
        self.wait(1)

        self.play(Transform(text_slope[1], text_2x))

        self.wait(20)
