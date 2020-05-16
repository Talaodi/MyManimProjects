from manimlib.imports import *


class Integral(GraphScene):
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

        start_line = Line(self.input_to_graph_point(1, self.square_graph), self.coords_to_point(1, 0), color=YELLOW)
        end_line = Line(self.input_to_graph_point(3, self.square_graph), self.coords_to_point(3, 0), color=YELLOW)
        text_start = TexMobject("1").next_to(start_line, DOWN)
        text_end = TexMobject("3").next_to(end_line, DOWN)
        self.play(Write(VGroup(start_line, end_line, text_start, text_end)))
        self.wait(1)

        numbers = [3, 5, 10, 30, 60, 100]
        last = self.make_rectangles(1, 3)
        text_number = TextMobject("Number:1").next_to(VGroup(text_start, text_end), DOWN)
        text_dx = TextMobject("d$x$:2").next_to(text_number, DOWN)
        self.play(Write(VGroup(last, text_number, text_dx)))
        self.wait(1)

        for number in numbers:
            now = self.make_rectangles(1, 3, number)
            text_new_number = TexMobject(str(number)).next_to(text_number[0][6], RIGHT)
            text_new_dx = TexMobject("%.2f" % (2 / number)).next_to(text_dx[0][2], RIGHT)
            self.play(
                Transform(last, now),
                Transform(text_number[0][7], text_new_number),
                Transform(text_dx[0][3], text_new_dx)
            )
            self.wait(0.2)

        self.wait(1)
        text_sum = TexMobject("\\sum_i f(x_i){\\rm d}x \\approx %.2f" % (9 - 0.33)).next_to(text_dx, DOWN)
        text_int = TexMobject("\\int_1^3 f(x){\\rm d}x=\\frac{26}{3}").move_to(text_sum)
        self.play(Write(text_sum))
        self.wait(1)
        self.play(Transform(text_sum, text_int))

        self.wait(10)

    def make_rectangles(self, start, end, number=1):
        width = (self.coords_to_point(end, 0)[0] - self.coords_to_point(start, 0)[0]) / number
        size = (end - start) / number
        rectangles = VGroup(*(
            Rectangle(
                width=width, height=self.input_to_graph_point(
                    start + (i + 0.5) * size, self.square_graph
                )[1], color=BLUE
            ).next_to(
                self.coords_to_point(start + i * size, 0), RIGHT, aligned_edge=DOWN
            ).shift(number / 10 * LEFT * width).set_opacity(0.6).set_fill(color=BLUE)
            for i in range(0, number)
        ))

        return rectangles