import json
from collections import defaultdict

import numpy as np
import plotly.graph_objects as go
from matplotlib.colors import CSS4_COLORS

APPLICATIONS_PATH = "applications.json"


def css_color_to_rgba(color_name, alpha):
    try:
        hex_value = CSS4_COLORS[color_name.lower()]
        rgb = tuple(int(hex_value[i : i + 2], 16) for i in (1, 3, 5))
        rgba = (*rgb, alpha)
        return f"rgba{rgba}"
    except KeyError:
        return None


def create_neighbor_pairs(input_list):
    return [(input_list[i], input_list[i + 1]) for i in range(len(input_list) - 1)]


def main():
    with open(APPLICATIONS_PATH, "r") as file:
        applications = json.load(file)

    labels = set()
    links = defaultdict(int)

    for application in applications:
        application["links"] = [
            (application["process"][index], application["process"][index + 1])
            for index in range(len(application["process"]) - 1)
        ]
        labels.update(application["process"])

        for link in application["links"]:
            links[link] += 1

    labels = list(labels)
    edges = np.array(list(links.keys()))

    source = [labels.index(sourceLabel) for sourceLabel in edges[:, 0]]
    target = [labels.index(targetLabel) for targetLabel in edges[:, 1]]

    nodeColors = [
        (
            "lightgreen"
            if node not in ["Rejected", "No Answer", "Declined"]
            else "red" if node in ["Rejected", "No Answer"] else "yellow"
        )
        for node in labels
    ]

    linkColors = [
        (
            css_color_to_rgba("lightgreen", 0.5)
            if node not in ["Rejected", "No Answer", "Declined"]
            else (
                css_color_to_rgba("red", 0.5)
                if node in ["Rejected", "No Answer"]
                else css_color_to_rgba("yellow", 0.5)
            )
        )
        for node in edges[:, 1]
    ]

    value = list(links.values())

    link = dict(source=source, target=target, value=value, color=linkColors)
    node = dict(label=labels, pad=35, thickness=10, color=nodeColors)
    data = go.Sankey(link=link, node=node)
    fig = go.Figure(data=[data])

    fig.show()


if __name__ == "__main__":
    main()
