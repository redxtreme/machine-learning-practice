//generate a randomly sized population
//of neural nets
//score the best one
//best ones get to reproduce
//source: https://www.youtube.com/watch?v=0a-52ntK3T8

var ttt = function(ttt) {
    
    //three states
    var X;
    var O;
    var TIE;
    
    //helper classes
    function newBoard() {
        return 0;
    }
    
    function isEmpty(board) {
        return (board === 0);
    }
    
    function getPiece(board), square) {
        
        //opperate at the bit level
        //bitwise opperation
        //Take the square * 2 ^ 1
        //Board / (square * 2 ^ 1)
        //& multiplies them by 3
        return ((board >> (square << 1)) & 3);
    }
    
    function move(board, square, piece) {
        
        //ex.
        //0101
        //0111
        //after combined: 0111
        
        //combine these values
        return (board | (piece << (square << 1)));
    }
    
    //history is stored locally in a temp cache stack
    function Game(board, turn, history) {
        this.board = board;
        this.turn = turn;
        this.history = history;
    }
    
    //define prototypes
    
    //equals
    Game.prototype.equals = function Game_equals(other) {
        
        //does the board equal the next state and the turn is equal to the next turn
        var toReturn = (this.board === other.board && this.turn === other.turn);
        
        return toReturn;
    }
    
    Game.prototype.getPiece = function Game_getPiece(square) {
        return getPiece(this.board, square)
    }
    
    Game.prototype.move = function Game_move(square) {
        //push the new state of the board onto the history stack
        this.history.push(this.board);
        this.board = move(this.board, square, this.turn);
        
        //shift the bit to either the ai or player
        this.turn ^=2;
    }
    
    Game.prototype.undo = function Game_undo() {
        this.board = this.history.pop();
        
        //shift the bit to either the ai or player
        this.turn ^=2;
    }
    
    //declare winner
    Game.prototype.winner = function Game_winner(board) {
        return winner(this.board)
    }
    
    //draw the board on the canvas
    function drawBoard(ctx) {
        //initialize canvas
        ctx.beginPath();
        
        //draw the hatch lines
        ctx.moveTo(0.333, 0.05);
        ctx.lineTo(0.333, 0.95);
        ctx.moveTo(0.666, 0.05);
        ctx.lineTo(0.666, 0.95);
        ctx.moveTo(0.95, 0.333);
        ctx.lineTo(0.95, 0.666);
        ctx.stroke()
    }
}