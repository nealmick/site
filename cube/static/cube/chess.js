


positionStr="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


var board = null

var game = new Chess()
let history = [];
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')

var requesting = false
var back = false

function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for the side to move
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||(game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }
}

function onDrop (source, target) {
  // see if the move is legal
  
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null){
    console.log(game.fen())
    return 'snapback'

  }
  //if move was legal should be able to call new functions

  f = board.fen()
  

  console.log(history)

  //fasdf = requestMove('f','f',board.fen())
  fasdf = requestMove2(f,source,target)
  updateStatus()

}

function requestMove2(fen,source,target){
  requesting=true
  let fasdf = ''
  $.ajax(
    {
        type:"GET",
        url: "/chess/nextMoveSunFish/",
        async: true,
        
        dataType: 'json',
        data:{
          from: String(source),
          to: String(target),
          fen: String(board.fen())
        },
        success: function(asdf) {
            let fasdf = asdf.asdf

            history.push(fasdf)
            console.log('response:',fasdf)
            game.load(fasdf)
            //board.move(fasdf[0]+fasdf[1].toUpperCase()+'-'+ fasdf[2]+fasdf[3].toUpperCase() )
            board.position(game.fen())
            updateStatus ()
          requesting = false
      }
    })
    
    return fasdf 

}







// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  board.position(game.fen())
}

function updateStatus () {
  var status = ''

  var moveColor = 'White'
  if (game.turn() === 'b') {
    moveColor = 'Black'
  }

  // checkmate?
  if (game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.'
  }

  // draw?
  else if (game.in_draw()) {
    status = 'Game over, drawn position'
  }

  // game still on
  else {
    status = moveColor + ' is thinking'

    // check?
    if (game.in_check()) {
      status += ', ' + moveColor + ' is in check'
    }
  }
  
  $status.html(status)
  $fen.html(game.fen())
  $pgn.html(game.pgn())
}

var config = {
  draggable: true,
  position: positionStr,
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}
board = Chessboard('myBoard', config)
$(window).resize(board.resize)
updateStatus()
  
function moveBack(game){
    if(requesting){
      return game
    }else{
      board.position(history[history.length-2])
      game.load(history[history.length-2])
      history.pop();
      updateStatus ()
      back = true
      return game
  }
}





function newGame(){
  location.reload();


}


















/*

let board=createBoard()
chessBoard = positionStr
//board is 0-7x7 top left is 0x0 top right is 0x71
//bottom left is 7x0, bottom right is 7x7
board =updateBoard(positionStr)
console.log(board)
bigStr = printBoard(board)
console.log(bigStr)

document.getElementById('chessBoard').innerText = positionStr


function printBoard(board){
    bigStr = ''
    for(foo=0;foo<=7;foo++){
        for(oof=0;oof<=7;oof++){
            bigStr+=board[foo][oof]
        }
        bigStr+='\n'
    }
    return bigStr
}
//takes fen str and updates board array
function updateBoard(positionStr){
    x=0
    y=0
    for(foo=0;foo<positionStr.length;foo++){
        if(!isNaN(positionStr[foo])){
            x+=Number(positionStr[foo])
        }
        else if(positionStr[foo]=='/'){
            y++
            x=0
        }
        else if(positionStr[foo]==':'){
            break
        }
        else{
            board[y][x]=positionStr[foo]
            x++
        }
    }
    return board
}
//returns array representing board 
function createBoard(){
    let board=[]
    for(x=0;x<=7;x++){
        board.push([])
        for(y=0;y<=7;y++){
            board[x].push([])
            board[x][y]='_'
        }
    }
    return board
}

*/



function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


