import math

from uct import get_most_visited_child


def _get_board(state_or_node):
    if state_or_node is None:
        return None

    if hasattr(state_or_node, "board"):
        return list(state_or_node.board)

    state = getattr(state_or_node, "state", None)
    if state is not None and hasattr(state, "board"):
        return list(state.board)

    return None


def _format_board(board):
    if not board:
        return "(no board)"

    symbols = {1: "X", -1: "O", 0: " "}
    rows = []
    for row_index in range(3):
        row = board[row_index * 3:(row_index + 1) * 3]
        rows.append(f" {symbols[row[0]]} | {symbols[row[1]]} | {symbols[row[2]]} ")
        if row_index < 2:
            rows.append("---+---+---")
    return "\n".join(rows)


def _node_label(node):
    board = _get_board(node)
    visits = getattr(node, "visits", 0)
    move = getattr(node, "parent_action", None)
    move_text = f"move={move}" if move is not None else "root"

    if board is not None:
        board_text = " | ".join(str(cell) for cell in board)
        return f"{move_text} | visits={visits} | board=[{board_text}]"

    return f"{move_text} | visits={visits}"


def _child_summary(parent, child, selected_child=None):
    visits = getattr(child, "visits", 0)
    parent_visits = max(getattr(parent, "visits", 0), 1)
    current_player = getattr(getattr(parent, "state", None), "current_player", None)
    wins = child.results.get(current_player, 0) if current_player is not None else 0
    win_rate = (wins / visits) if visits else 0.0
    exploitation = win_rate
    exploration = 1.41 * math.sqrt(math.log(parent_visits) / visits) if visits > 0 else 0.0
    uct_score = exploitation + exploration
    move = getattr(child, "parent_action", None)
    move_text = f"move={move}" if move is not None else "root"

    if child is selected_child:
        reason = "selected: most visited"
        marker = "●"
    else:
        reason = "candidate"
        marker = "○"

    return (
        f"{marker} {move_text}\n"
        f"   visits={visits} | wins_for_player={wins} | win_rate={win_rate:.2f} | "
        f"uct={uct_score:.2f}\n"
        f"   reason: {reason}"
    )


def _render_tree(node, depth=0, prefix="", max_depth=3, top_children=3, selected_child=None):
    if node is None:
        return

    print(prefix + _node_label(node))

    if depth >= max_depth:
        return

    children = list(getattr(node, "children", []) or [])
    if top_children is not None:
        children = sorted(children, key=lambda child: getattr(child, "visits", 0), reverse=True)[:top_children]

    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        branch = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")
        print(child_prefix + branch + _child_summary(node, child, selected_child).splitlines()[0])
        for line in _child_summary(node, child, selected_child).splitlines()[1:]:
            print(child_prefix + "    " + line)

        _render_tree(
            child,
            depth + 1,
            child_prefix + ("    " if is_last else "│   "),
            max_depth=max_depth,
            top_children=top_children,
            selected_child=selected_child,
        )


def visualize_mcts_tree(node, max_depth: int = 3, top_children: int = 3,
                        save: bool = False, filename=None, dpi: int = 150):
    """Render a structured terminal-based view of the current game state and the top explored children."""
    current_board = _get_board(node)
    selected_child = get_most_visited_child(node) if hasattr(node, "children") else None

    print("\n" + "=" * 70)
    print("MCTS VIEW")
    print("=" * 70)

    if current_board is not None:
        print("\nCurrent board:")
        print(_format_board(current_board))
    else:
        print("\nCurrent state has no board")

    if hasattr(node, "children") and hasattr(node, "state"):
        print(f"\nTop {top_children} explored children (depth {max_depth}):")
  
        _render_tree(node, max_depth=max_depth, top_children=top_children, selected_child=selected_child)
    elif current_board is not None:
        print("\nNo child tree available for this node.")

    if save:
        print(f"[visualization] save=True was requested for {filename or 'mcts_tree'} but terminal mode is active.")
