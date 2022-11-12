import matplotlib.pyplot as plt

FIG_X = 10
FIG_Y = 5
COLOR_LIST = ['black', 'blue', 'gold' , 'green', 'orange', 'red', 'white', 'yellow']



def bar_plot(elements: dict, title: str = None, 
            x_label: str = None, y_label: str = None,
            color: str = 'blue') -> None:

    x_elements: list = list(elements.keys())
    y_elements: list = list(elements.values())
    bar_color = color if color in COLOR_LIST else 'blue'

    fig = plt.figure(figsize = (FIG_X, FIG_Y))
    plt.bar(x_elements, y_elements, color=bar_color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.show()

    print(type(x_elements))
    print(type(y_elements))


   
