MIN_SIZE = 2
MAX_SIZE = 50
SIZE_QUESTION = f"So, what size of maze would you like ({MIN_SIZE}...{MAX_SIZE})? "
SIZE_ERROR = f"\tHmm. That's not quite between {MIN_SIZE} and {MAX_SIZE}, is it? Try again!"
TYPE_QUESTION = f"What about the maze type? A maze with a single (s) or multiple (m) solutions? "
TYPE_ERROR = f"\tThat's not an s nor an m!"
WELCOME_TITLE = "WELCOME TO THE MAZE"
WELCOME = [
    "\t*********************************************************************************",
    f"\t                             {WELCOME_TITLE}",
    "\t            the program for creating, playing and solving mazes",
    "\t*********************************************************************************",

]

INSTRUCTIONS = [
    [
        "\n\tMAZE PARAMETERS:",
        "\tTo start with, you will be asked for the edge size and the type of the maze.",
        f"\tThe edge size N of the maze (N x N) can have any value in range {MIN_SIZE}...{MAX_SIZE}.",
        "\tThe type of the maze refers to the number of solutions the maze has:",
        "\t\t- a single solution (i.e. only one path from start to finish exists)",
        "\t\t- multiple solutions (i.e. many paths with varying lengths exist"
    ],
    [
        "\n\tMAZE GENERATION:",
        "\tThe maze will be generated using the Twist & Merge algorithm.",
        "\tYou can select to view the progress of the maze generation process live in a GUI.",
        "\n\tPLAYING THE MAZE:",
        "\tOnce the maze is ready, you are offered the option to try to solve it yourself.",
        "\tThe GUI will guide you on how to move within the maze.",
    ],
    [
        "\n\tSOLVING THE MAZE:",
        "\tSeveral more or less different algorithms are available for solving the maze.",
        "\tYou can select to view the solving process live, or just jump to the solution.",
        "\tThe available algorithms are:",
        "\t\t- Dijkstra",
        "\t\t- AStar",
        "\t\t- Wall follower",
        "\t\t- Dead end filler",
        "\t\t- IDAStar",
        "\t\t- Fringe",
    ],
    [
        "\n\tGENERAL:",
        "\tPlease note that the GUI will only answer to keystrokes.",
        "\tTyping 'q' enables you to quit this program at this point.\n"
    ]
]
