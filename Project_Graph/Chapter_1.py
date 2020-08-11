from manimlib.imports import *


class Graph(Scene):

    def construct(self):
        self.make_graph()
        self.intro()
        self.graph()
        self.top()
        self.prim()
        self.dijkstra()
        text_end = TextMobject("$Thanks$").scale(2.25)
        self.play(Write(text_end))
        self.wait(3)
        self.play(FadeOut(text_end))
        self.wait(1)

    def intro(self):
        text_intro = TextMobject(
            "图论总结（一）", color=RED).scale(2.25).shift(UP * 0.5)
        text_producer = TextMobject(
            "By Talaodi", color=YELLOW).shift(DOWN * 1.25).scale(1.25)
        text_copy_right = TextMobject(
            "使用 Python + Manim 制作").move_to(BOTTOM).scale(0.8).shift(0.6 * UP)

        self.play(Write(text_intro))
        self.wait(0.3)
        self.play(Write(text_producer), Write(text_copy_right))
        self.wait(1)

        self.play(FadeOut(text_producer))
        self.wait(0.1)
        self.play(FadeOut(VGroup(text_intro, text_copy_right)))
        self.wait(1)

    def graph(self):
        text_G = TexMobject("G(N,E)").scale(3)

        text_G_nodes = TexMobject("Nodes").scale(
            3).next_to(text_G[0][1]).shift(2 * LEFT)
        text_G_edges = TexMobject("Edges").scale(3)
        G_real_nodes = self.nodes.copy().scale(
            0.125).next_to(text_G[0][1]).shift(2 * LEFT)
        G_real_edges = self.edges.copy().scale(0.125)

        self.play(Write(text_G))
        self.wait(1)

        self.play(text_G[0][3:].next_to, text_G_nodes, text_G[0][0:2].next_to,
                  text_G_nodes, LEFT, Transform(text_G[0][2], text_G_nodes))
        self.wait(1)

        self.play(text_G[0][3:].next_to, G_real_nodes, text_G[0][0:2].next_to,
                  G_real_nodes, LEFT, Transform(text_G[0][2], G_real_nodes))
        self.wait(1)

        text_G_edges.next_to(text_G[0][3], aligned_edge=DOWN)
        self.play(text_G[0][5:].next_to, text_G_edges,
                  Transform(text_G[0][4], text_G_edges))
        self.wait(1)

        G_real_edges.move_to(text_G_edges)
        self.play(Transform(text_G[0][4], G_real_edges), text_G[0][5:].next_to,
                  G_real_edges, text_G[0][:4].next_to, G_real_edges, LEFT)
        self.wait(1)

        self.play(FadeOut(VGroup(text_G[0][1], text_G[0][3], text_G[0][5])),
                  Transform(text_G[0][2], self.nodes.copy().scale(
                      0.875).shift(0.775 * UP)),
                  Transform(text_G[0][4], self.edges.copy().scale(
                      0.875).shift(0.775 * UP)),
                  text_G[0][0].move_to, BOTTOM + 0.75 * UP, Transform(text_G[0][0], TexMobject("Graph").move_to(BOTTOM + 0.75 * UP).scale(3), run_time=2.5))
        self.nodes_after_graph = text_G[0][2]
        self.edges_after_graph = text_G[0][4]
        self.wait(3)
        self.play(FadeOut(VGroup(self.nodes_after_graph,
                                 self.edges_after_graph, text_G[0][0])))

    def top(self):
        nodes = self.nodes.copy().scale(0.875).shift(0.775 * UP)
        edges = self.edges.copy().scale(0.875).shift(0.775 * UP)
        self.play(FadeIn(VGroup(nodes, edges)))
        self.wait(2)
        topsort = [1, 2, 4, 6, 5, 3, 7, 10, 12, 11, 9, 8]
        used = [False for i in range(15)]

        def add_and_delete(self, index_of_node, last_text, new_com, new, new_line=False):
            nonlocal nodes, edges, used
            node = nodes[index_of_node]
            self.play(node[0].set_color, ORANGE)
            self.wait(1)
            edges_make_non = list()
            for i in range(15):
                if (index_of_node + 1 in self.edges_number[i][:2] and not used[i]):
                    edges_make_non.append(edges[i])
                    used[i] = True

            if new:
                self.play(FadeOut(VGroup(*edges_make_non)),
                          node.move_to, BOTTOM + 0.75 * UP + 3.5 * LEFT)
                last_text = VGroup(node)
            elif new_com:
                com = TexMobject(",").next_to(last_text[-1])
                if not new_line:
                    temp_node = node.copy().next_to(com)
                    com.next_to(last_text[-1], aligned_edge=DOWN)
                    self.play(FadeOut(VGroup(*edges_make_non)),
                              FadeIn(com), node.move_to, temp_node)
                else:
                    com.next_to(last_text, aligned_edge=DOWN)
                    self.play(FadeOut(VGroup(*edges_make_non)), FadeIn(com),
                              node.next_to, last_text[0], DOWN, aligned_edge=LEFT)

                last_text.add(com).add(node)

            self.wait(1)
            return last_text

        text_top = add_and_delete(self, 0, None, None, True)
        for i in range(1, 6):
            text_top = add_and_delete(
                self, topsort[i] - 1, text_top, True, False)

        self.play(VGroup(*(nodes[topsort[i] - 1] for i in range(6, 12))).shift, UP, VGroup(
            *(edges[i] for i in range(15) if not used[i])).shift, UP, text_top.shift, UP)
        text_top = add_and_delete(
            self, topsort[6] - 1, text_top, True, False, True)

        for i in range(7, 12):
            text_top = add_and_delete(
                self, topsort[i] - 1, text_top, True, False)

        self.play(text_top.shift, 3.5 * UP, text_top.scale, 1.75, run_time=2)

        text_topsort = TextMobject(
            "Topological-sort").scale(2.5).next_to(text_top, DOWN).shift(DOWN)
        self.play(Write(text_topsort), run_time=2)
        self.wait(3)
        self.play(FadeOut(VGroup(text_topsort, text_top)))

    def prim(self):
        nodes = self.nodes.copy()

        def make_arrow(s, t): return DoubleArrow(self.nodes[s - 1][0].get_arc_center(), self.nodes[t - 1][0].get_arc_center(),
                                                 buff=0.5, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        edges = VGroup(*(VGroup(make_arrow(self.edges_number[i][0], self.edges_number[i][1]).set_opacity(0.6),
                                TexMobject("%d" % self.edges_number[i][2], color=ORANGE).move_to(self.edges.copy()[i])) for i in range(15)))
        graph = VGroup(nodes, edges).scale(0.8).shift(UP)
        self.play(FadeIn(graph))
        self.wait(1)
        text_list = [0] + ["$\infty$"] * 11

        text_start = TextMobject("start: 1").next_to(
            graph, DOWN, aligned_edge=LEFT).shift(2 * LEFT + 0.5 * DOWN).scale(1.25)
        self.play(Write(text_start, run_time=1))
        form = VGroup(*(VGroup(Square(side_length=0.8), TextMobject(text_list[i]), TextMobject("%d" % (i + 1))) for i in range(12))
                      ).arrange(buff=0).next_to(text_start)
        for sq in form:
            sq[2].next_to(sq[0], DOWN, buff=0.15)

        self.play(FadeIn(form))
        self.wait(1)
        self.play(nodes[0][0].set_color, BLUE, form[0].set_fill, {
                  "opacity": 0.6}, form[0].set_fill, GRAY)
        last_node = 0
        used = [True] + 11 * [False]
        choosed = [False] * 15

        def set_color_and_add():
            nonlocal last_node, choosed
            index_of_edge = (i for i in range(
                15) if last_node + 1 in self.edges_number[i][:2])
            trans = ([], [])
            light = list()
            for i in index_of_edge:
                edge = self.edges_number[i]
                to = edge[1] if used[edge[0] - 1] else edge[0]
                ptr = edge[0] if used[edge[0] - 1] else edge[1]
                value = edge[2]
                if (not used[to - 1]):
                    light.append(edges[i][0])
                    if text_list[to - 1] == "$\infty$":
                        text_list[to - 1] = str(value)
                        trans[0].append(form[to - 1][1])
                        trans[1].append(TexMobject(
                            text_list[to - 1]).move_to(form[to - 1][1]))
                    elif value < int(text_list[to - 1]):
                        text_list[to - 1] = str(value)
                        trans[0].append(form[to - 1][1])
                        trans[1].append(TexMobject(
                            text_list[to - 1]).move_to(form[to - 1][1]))

            _min = 1 << 31
            index = 0
            for i in range(12):
                if (text_list[i] != "$\infty$") and not used[i]:
                    if (int(text_list[i]) < _min):
                        _min = int(text_list[i])
                        index = i
            index_of_node = index
            print(index_of_node)
            index_of_choose_edge = [i for i in range(15) if True in ([last_node + 1, index_of_node + 1] in (self.edges_number[i][:2], self.edges_number[i][:2][::-1])
                                                                     for last_node in range(12) if used[last_node])][0]

            choosed[index_of_choose_edge] = True

            data = self.edges_number[index_of_choose_edge]
            transform = None
            def make_edge(s, t): return Arrow(nodes[s - 1][0].get_arc_center(), nodes[t - 1][0].get_arc_center(),
                                              buff=0.5, stroke_width=3, max_tip_length_to_length_ratio=0.15, color=BLUE).set_opacity(0.6)

            if (used[data[1] - 1]):
                transform = make_edge(data[1], data[0])
            else:
                transform = make_edge(data[0], data[1])
            self.play(VGroup(*light).set_color, BLUE)
            self.wait(1)
            self.play(Transform(VGroup(*trans[0]), VGroup(*trans[1])))
            self.play(VGroup(*(light)).set_color, WHITE,
                      Transform(edges[index_of_choose_edge][0], transform),
                      nodes[index_of_node][0].set_color, BLUE,
                      form[last_node].set_color, WHITE,
                      form[index_of_node].set_color, YELLOW,
                      form[index_of_node].set_fill, {"opacity": 0.6},
                      form[index_of_node].set_fill, GRAY)

            used[index_of_node] = True
            last_node = index_of_node

        for i in range(11):
            set_color_and_add()

        text_53 = TexMobject("sum=53").scale(2).move_to(form)
        text_prim = TextMobject(
            "$Prim$(to find the $MST$)").scale(2).move_to(form)

        self.wait(2)

        self.play(Transform(VGroup(form, text_start), text_53))
        self.wait(1.5)
        self.play(Transform(VGroup(form, text_start), text_prim, run_time=1.5))

        self.wait(3)
        self.play(FadeOut(VGroup(graph, VGroup(form, text_start))))

    def dijkstra(self):
        nodes = self.nodes.copy()

        def make_arrow(s, t): return Arrow(self.nodes[s - 1][0].get_arc_center(), self.nodes[t - 1][0].get_arc_center(),
                                           buff=0.5, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        edges = VGroup(*(VGroup(make_arrow(self.edges_number[i][0], self.edges_number[i][1]).set_opacity(0.6),
                                TexMobject("%d" % self.edges_number[i][2], color=ORANGE).move_to(self.edges.copy()[i])) for i in range(15)))

        graph = VGroup(nodes, edges).scale(0.8).shift(UP)
        self.play(FadeIn(graph))
        self.wait(1)
        text_list = [0] + 11 * ["$\infty$"]
        text_start = TextMobject("start: 1").next_to(
            graph, DOWN, aligned_edge=LEFT).shift(2 * LEFT + 0.5 * DOWN).scale(1.25)
        self.play(Write(text_start, run_time=1))
        form = VGroup(*(VGroup(Square(side_length=0.8), TextMobject(text_list[i]), TextMobject("%d" % (i + 1))) for i in range(12))
                      ).arrange(buff=0).next_to(text_start)
        for sq in form:
            sq[2].next_to(sq[0], DOWN, buff=0.15)

        self.play(FadeIn(form))
        self.wait(1)
        self.play(nodes[0][0].set_color, BLUE, form[0].set_fill, {
                  "opacity": 0.6}, form[0].set_fill, GRAY)
        last_node = 0
        used = [True] + 11 * [False]
        father = [0] * 12
        paths = [None] * 12

        def set_color_and_add():
            nonlocal last_node, paths
            index_of_edge = (i for i in range(
                15) if last_node + 1 == self.edges_number[i][0])
            trans = ([], [])
            light = list()
            for i in index_of_edge:
                edge = self.edges_number[i]
                to = edge[1]
                ptr = edge[0]
                value = edge[2]
                if (not used[to - 1]):
                    light.append(edges[i][0])
                    if text_list[to - 1] == "$\infty$":
                        father[to - 1] = ptr
                        text_list[to -
                                  1] = str(int(text_list[ptr - 1]) + value)
                        trans[0].append(form[to - 1][1])
                        trans[1].append(TexMobject(
                            text_list[to - 1]).move_to(form[to - 1][1]))
                    elif int(text_list[ptr - 1]) + value < int(text_list[to - 1]):
                        father[to - 1] = ptr
                        text_list[to -
                                  1] = str(int(text_list[ptr - 1]) + value)
                        trans[0].append(form[to - 1][1])
                        trans[1].append(TexMobject(
                            text_list[to - 1]).move_to(form[to - 1][1]))
            _min = 1 << 31
            index = -1
            for i in range(12):
                if (text_list[i] != "$\infty$") and not used[i]:
                    if (int(text_list[i]) < _min):
                        _min = int(text_list[i])
                        index = i
            if index == -1:
                return False

            index_of_node = index
            set_color_edges_index = list()
            while (father[index]):
                print([father[index], index + 1])
                for i in range(15):
                    if [father[index], index + 1] == self.edges_number[i][:2]:
                        print(i)
                        set_color_edges_index.append(i)
                        break
                index = father[index] - 1

            paths[index_of_node] = set_color_edges_index
            self.play(VGroup(*light).set_color, BLUE)
            self.wait(1)
            self.play(Transform(VGroup(*trans[0]), VGroup(*trans[1])))
            self.play(VGroup(*(light)).set_color, WHITE,
                      VGroup(*(edges[i][0]
                               for i in set_color_edges_index)).set_color, BLUE,
                      nodes[index_of_node][0].set_color, BLUE,
                      form[last_node].set_color, WHITE,
                      form[index_of_node].set_color, YELLOW,
                      form[index_of_node].set_fill, {"opacity": 0.6},
                      form[index_of_node].set_fill, GRAY)
            if set_color_edges_index:
                self.wait(1)
                self.play(
                    VGroup(*(edges[i] for i in set_color_edges_index)).set_color, WHITE)

            used[index_of_node] = True
            last_node = index_of_node

            return True

        for i in range(11):
            if not set_color_and_add():
                break
        self.play(form[last_node].set_color, WHITE)
        self.wait(1)

        print(len(paths))

        for i in range(1, 12):
            if used[i]:
                print(i, i, i)
                self.play(form[i].set_color, YELLOW)
                self.play(VGroup(*(edges[i][0]
                                   for i in paths[i])).set_color, BLUE)
                self.wait(1)
                self.play(form[i].set_color, WHITE, VGroup(
                    *(edges[i][0] for i in paths[i])).set_color, WHITE)
                self.wait(1)

        self.wait(1)
        text_dij = TextMobject(
            "$Dijkstra$(to find the $SP$)").scale(2).move_to(form)
        self.play(Transform(VGroup(text_start, form), text_dij, run_time=1.5))
        self.wait(3)
        self.play(FadeOut(VGroup(graph, VGroup(text_start, form))))

    def make_graph(self):
        nodes = list()

        def make_nodes(u, l, i): return VGroup(Circle().shift(
            u * UP + l * LEFT).scale(0.4), TextMobject("%d" % i, color=YELLOW).shift(u * UP + l * LEFT))

        self.nodes_number = [
            [1.6, 2.65], [3.2, 1.5], [3.25, -3.05], [0.2, -2.2], [1.65, -5.85],
            [-2.45, -4.35], [-0.2, 0.7], [-2.9, -1.25], [-0.8, 2.8], [-3.1, 1],
            [-2.7, 3.9], [1.5, 5.32]
        ]

        i = 0
        for node in self.nodes_number:
            i += 1
            nodes.append(make_nodes(node[0], node[1], i))

        edges = list()

        def make_edges(s, t): return Arrow(nodes[s - 1][0].get_arc_center(), nodes[t - 1][0].get_arc_center(),
                                           buff=0.5, stroke_width=3, max_tip_length_to_length_ratio=0.15)

        self.edges_number = [
            [1, 2, 3], [2, 12, 5], [5, 3, 2], [4, 3, 9], [1, 3, 4], [4, 5, 7],
            [6, 5, 2], [4, 6, 1], [4, 7, 12], [1, 9, 14], [6, 8, 4], [9, 8, 9],
            [10, 9, 10], [11, 9, 12], [12, 11, 1]
        ]

        for point in self.edges_number:
            edges.append(make_edges(point[0], point[1]))

        self.nodes = VGroup(*nodes)
        self.edges = VGroup(*edges)
