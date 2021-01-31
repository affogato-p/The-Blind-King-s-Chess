# The Blind King's Chess
## Just like traditional chess, except that there is line of sight AND your king is **blind**.
A variation of chess implementing limited vision. Players will not be able to see what is on the board beyond the line of sight of their pieces. The line of sight of each piece is determined by the tiles it can move to. The line of sight of a piece can be obstructed by an enemy piece blocking the path.

## Rules:
1. Players are able to see parts of the board which their pieces' line of sight does not cover.
2. Pawns can move both forward and backward. For their first move they can advance two tiles instead of one.
3. The king is **blind**. The king can only see what other pieces see, he has no vision of his own, and the king can only move to visible tiles within a 3x3 tile-space.
4. Pawns are promoted unconditonally to Queens after they reach the other end.
5. The Knight piece not only reveals the tiles it can move to but also the tiles in a one-tile radius around it, except directly in front and behind it. The only piece in the game that doesn't have its vision blocked by other pieces.
6. All other rules of chess apply.

*This game is programmed in Python using the pygame library.*
