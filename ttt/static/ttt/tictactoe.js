


console.log('tictactoe')


let winner = '_'
let board_ = [];

let state = 1

board_ =createboard_(board_,x,y)


console.log(board_)




    

printboard_()


function restart(){
  location.reload();

}




function getMove(board_){
    let fasdf = prepareSend(board_)
    state=2
    $.ajax(
      {
          type:"GET",
          url: "/tictactoe/ttt/move/",
          
          dataType: 'json',
          data:{
            asdf: String(fasdf),
          },
          success: function(asdf) {
            let res = asdf.asdf
            rw = String(asdf.winner)
  
            
            //console.log('response:',res)
            updateboard_(board_,res)
            printboard_()
            updateView(board_)
            if(rw=='x' || rw =='o'){
                document.getElementById("winner").innerText = 'winner is: '+rw
                winner = rw
            }
            if(rw=='t'){
                document.getElementById("winner").innerText = 'Tie Game!'
                winner = rw
            }

            state = 1

            //board_.move(fasdf[0]+fasdf[1].toUpperCase()+'-'+ fasdf[2]+fasdf[3].toUpperCase() )
            
  
        }
      })

      return winner
  
  }



function updateView(board_){
    count=1;
    for(foo=0;foo<x;foo++){
        for(oof=0;oof<y;oof++){
            if(board_[foo][oof]!='_'){
                document.getElementById("box"+String(count)).innerText = board_[foo][oof]
            }
            count++

        }
    }


}

function updateboard_(board_,fasdf){

    let counter = 0;
    for(foo=0;foo<x;foo++){
        for(oof=0;oof<y;oof++){

            if(fasdf[counter]!='_'){
                board_[foo][oof]=fasdf[counter]
            }
            counter++
            
        }
    }

    return board_
}

function prepareSend(board_){
    let sendString = '';

    for(foo=0;foo<x;foo++){
       
        for(oof=0;oof<y;oof++){
            sendString+=board_[foo][oof]
        }

    }
    return sendString   


}






function printboard_(){
    let pString = "";
    let bigString ="";
    for(foo=0;foo<x;foo++){
       
        for(oof=0;oof<y;oof++){
            pString+=board_[foo][oof]
        }
        bigString+=pString+'\n'
        pString = "";
    }
    //console.log(bigString)
}

function createboard_(board_,x,y){
    
    for(foo=0;foo<x;foo++){
        board_.push([]);
        for(oof=0;oof<y;oof++){
            board_[foo].push('_')
        }
    }
    return board_
}


function box1(){
    if (board_[0][0]=='_'&& winner=='_'&& state==1){
        document.getElementById("box1").innerText = 'x'
        board_[0][0]='x'
        printboard_()
        getMove(board_)
    }
}

function box2(){
    if (board_[0][1]=='_'&& winner=='_'&& state==1){
      document.getElementById("box2").innerText = 'x'
        board_[0][1]='x'
        printboard_()
        getMove(board_)
    }
}
function box3(){
    if (board_[0][2]=='_'&& winner=='_'&& state==1){
        document.getElementById("box3").innerText = 'x'
        board_[0][2]='x'
        printboard_()
        getMove(board_)
    }
}
function box4(){
    if (board_[1][0]=='_'&& winner=='_'&& state==1){
        document.getElementById("box4").innerText = 'x'
        board_[1][0]='x'
        printboard_()
        getMove(board_)
    }
}
function box5(){
    if (board_[1][1]=='_'&& winner=='_'&& state==1){
        document.getElementById("box5").innerText = 'x'
        board_[1][1]='x'
        printboard_()
        getMove(board_)
    }
}
function box6(){
    if (board_[1][2]=='_'&& winner=='_'&& state==1){

        document.getElementById("box6").innerText = 'x'
        board_[1][2]='x'
        printboard_()
        getMove(board_)
    }
}
function box7(){
    if (board_[2][0]=='_'&& winner=='_'&& state==1){

        document.getElementById("box7").innerText = 'x'
        board_[2][0]='x'
        printboard_()
        getMove(board_)
    }
}
function box8(){
    if (board_[2][1]=='_'&& winner=='_'&& state==1){

        document.getElementById("box8").innerText = 'x'
        board_[2][1]='x'
        printboard_()
        getMove(board_)
    }
}
function box9(){
    if (board_[2][2]=='_'&& winner=='_'&& state==1){
        document.getElementById("box9").innerText = 'x'
        board_[2][2]='x'
        printboard_()
        getMove(board_)
    }
}

