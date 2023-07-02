

var whiteRookP = $('<img>', {
  src: "static/img/Chess_tile_rl-whitebg.svg.png",
  class: 'piece rook replace' // You can add additional classes if needed
});

var whiteBishopP = $('<img>', {
  src: "static/img/240px-Chess_tile_bl.svg.png",
  class: 'piece bishop replace' // You can add additional classes if needed
});

var whiteQueenP = $('<img>', {
  src: "static/img/Chess_tile_ql-whitebg.svg.png",
  class: 'piece queen replace' // You can add additional classes if needed
});

var whiteKnightP = $('<img>', {
  src: "static/img/Chess_tile_nl.svg.png",
  class: 'piece knight replace' // You can add additional classes if needed
});

var blackQueenP = $('<img>', {
  src: "static/img/Chess_tile_qd.svg.png",
  class: 'piece knight replace' // You can add additional classes if needed
});

var blackBishopP = $('<img>', {
  src: "static/img/Chess_tile_bd.svg.png",
  class: 'piece knight replace' // You can add additional classes if needed
});

var blackRookP = $('<img>', {
  src: "static/img/Chess_tile_rd.svg.png",
  class: 'piece knight replace' // You can add additional classes if needed
});

var blackKnightP = $('<img>', {
  src: "static/img/240px-Chess_tile_nd.svg.png",
  class: 'piece knight replace' // You can add additional classes if needed
});


var whiteRook = $('<img>', {
  src: "static/img/Chess_tile_rl-whitebg.svg.png",
  class: 'piece rook' // You can add additional classes if needed
});

var whiteBishop = $('<img>', {
  src: "static/img/240px-Chess_tile_bl.svg.png",
  class: 'piece bishop' // You can add additional classes if needed
});

var whiteQueen = $('<img>', {
  src: "static/img/Chess_tile_ql-whitebg.svg.png",
  class: 'piece queen' // You can add additional classes if needed
});

var whiteKnight = $('<img>', {
  src: "static/img/Chess_tile_nl.svg.png",
  class: 'piece knight' // You can add additional classes if needed
});

var blackQueen = $('<img>', {
  src: "static/img/Chess_tile_qd.svg.png",
  class: 'piece knight' // You can add additional classes if needed
});

var blackBishop = $('<img>', {
  src: "static/img/Chess_tile_bd.svg.png",
  class: 'piece knight' // You can add additional classes if needed
});

var blackRook = $('<img>', {
  src: "static/img/Chess_tile_rd.svg.png",
  class: 'piece knight' // You can add additional classes if needed
});

var blackKnight = $('<img>', {
  src: "static/img/240px-Chess_tile_nd.svg.png",
  class: 'piece knight' // You can add additional classes if needed
});



$(document).ready(function() {
    $('.square').click(function() {
        var squareId = $(this).data('square');

        // Make an AJAX POST request to the Flask route
        $.ajax({
            type: 'POST',
            url: '/square',
            data: { square: squareId },
            success: function(response) {
                $('.clicked-square').removeClass('clicked-square');
                // write code to move
                if(response.includes("pro w")){
                    //            return "pro wr " + str(col) + " " + str(promotePawn[1])
                    let piece;
                    if(response[5] === "r"){
                        piece = whiteRook;
                    }
                    if(response[5] === "b"){
                        piece = whiteBishop;
                    }
                    if(response[5] === "k") {
                        piece = whiteKnight;
                    }
                    if(response[5] === "q"){
                        piece = whiteQueen;
                    }
                    let col = parseInt(response[7])+1;
                    let pCol = parseInt(response[9])+1
                    $('#8'+col).empty();
                    $("#8"+col).append(piece)
                    $('#7'+pCol).empty();
                    $('#7' + col + ' .replace').remove();
                    $('#6' + col + ' .replace').remove();
                    $('#5' + col + ' .replace').remove();
                    $('#7' + col + ' img').show();
                    $('#6' + col + ' img').show();
                    $('#5' + col + ' img').show();
                }
                else if (response.includes("res w")){
                    let col = parseInt(response[5])+1;
                    $('#8' + col + ' .replace').remove();
                    $('#5' + col + ' .replace').remove();
                    $('#6' + col + ' .replace').remove();
                    $('#7' + col + ' .replace').remove();
                    $('#8' + col + ' img').show();
                    $('#7' + col + ' img').show();
                    $('#6' + col + ' img').show();
                    $('#5' + col + ' img').show();

                }
                if(response.includes("pro b")){
                    //            return "pro wr " + str(col) + " " + str(promotePawn[1])
                    let piece;
                    if(response[5] === "r"){
                        piece = blackRook;
                    }
                    if(response[5] === "b"){
                        piece = blackBishop;
                    }
                    if(response[5] === "k") {
                        piece = blackKnight;
                    }
                    if(response[5] === "q"){
                        piece = blackQueen;
                    }
                    let col = parseInt(response[7])+1;
                    let pCol = parseInt(response[9])+1
                    $('#1'+col).empty();
                    $("#1"+col).append(piece)
                    $('#2'+pCol).empty();
                    $('#2' + col + ' .replace').remove();
                    $('#3' + col + ' .replace').remove();
                    $('#4' + col + ' .replace').remove();
                    $('#2' + col + ' img').show();
                    $('#3' + col + ' img').show();
                    $('#4' + col + ' img').show();
                }
                 else if (response.includes("res b")){
                    let col = parseInt(response[5])+1;
                    $('#1' + col + ' .replace').remove();
                    $('#4' + col + ' .replace').remove();
                    $('#3' + col + ' .replace').remove();
                    $('#2' + col + ' .replace').remove();
                    $('#1' + col + ' img').show();
                    $('#2' + col + ' img').show();
                    $('#3' + col + ' img').show();
                    $('#4' + col + ' img').show();
                }
                else if(response.includes("bp")){ // black promote
                     let col = parseInt(response[0])+1;
                    //alert(col)
                    $('#1'+col+" img").hide();
                    $('#2'+col+" img").hide();
                    $('#3'+col+" img").hide();
                    $('#4'+col+" img").hide();
                    $('#1'+col).append(blackQueenP);
                    $('#2'+col).append(blackRookP);
                    $('#3'+col).append(blackBishopP);
                    $('#4'+col).append(blackKnightP);
                }else if (response.includes("wp")){ // white promote
                    let col = parseInt(response[0])+1;
                    //alert(col)
                    $('#8'+col+" img").hide();
                    $('#7'+col+" img").hide();
                    $('#6'+col+" img").hide();
                    $('#5'+col+" img").hide();
                    $('#8'+col).append(whiteQueenP);
                    $('#7'+col).append(whiteRookP);
                    $('#6'+col).append(whiteBishopP);
                    $('#5'+col).append(whiteKnightP);
                }else if (response.includes("we")){ // white enpassant
                     $('.clicked-square').removeClass('clicked-square');
                    let pR = 8-parseInt(response[2])
                    let pC = parseInt(response[3])+1
                    let row = 8-parseInt(response[5])
                    let col = parseInt(response[6])+1
                    let pId = pR.toString()+pC.toString()
                    let id = row.toString()+col.toString()
                    var imageElement = $("#"+pId).find('img');
                    $('#'+pId).empty();
                    $('#'+id).empty();
                    $('#'+id).append(imageElement);
                    $('#'+(parseInt(row)-1).toString()+col).empty();

                }else if (response.includes("be")){
                     $('.clicked-square').removeClass('clicked-square'); // black en passant
                    let pR = 8-parseInt(response[2])
                    let pC = parseInt(response[3])+1
                    let row = 8-parseInt(response[5])
                    let col = parseInt(response[6])+1
                    let pId = pR.toString()+pC.toString()
                    let id = row.toString()+col.toString()
                    var imageElement = $("#"+pId).find('img');
                    $('#'+pId).empty();
                    $('#'+id).empty();
                    $('#'+id).append(imageElement);
                    $('#'+(parseInt(row)+1).toString()+col).empty();
                }else if (response == "1 1"){//white short
                    var imageElement = $("#18").find('img');
                    $("#18").empty()
                    $('#16').append(imageElement);
                    imageElement =  $("#15").find('img');
                    $("#15").empty()
                    $('#17').append(imageElement);
                }else if (response == "1 2"){ // white long
                    var imageElement = $("#11").find('img');
                    $("#11").empty()
                    $('#14').append(imageElement);
                    imageElement =  $("#15").find('img');
                    $("#15").empty()
                    $('#13').append(imageElement);
                }else if (response == "1 3"){ //black short
                    var imageElement = $("#88").find('img');
                    $("#88").empty()
                    $('#86').append(imageElement);
                    imageElement =  $("#85").find('img');
                    $("#85").empty()
                    $('#87').append(imageElement);
                }else if (response == "1 4"){ // black long
                    var imageElement = $("#81").find('img');
                    $("#81").empty()
                    $('#84').append(imageElement);
                    imageElement =  $("#85").find('img');
                    $("#85").empty()
                    $('#83').append(imageElement);
                }else if (response[0] === "0"){ // darken all the possible moves
                    let moves = []
                    for(var i = 2;i<response.length;i = i+3){
                        moves.push([parseInt(response[i]),parseInt(response[i+1])])
                    }
                    $('.clicked-square').removeClass('clicked-square');
                    // Iterate over the moves and process them
                    for (var i = 0; i < moves.length; i++) {
                        var move = moves[i];
                        var row = 8-move[0];
                        var col = move[1]+1;
                        let id = row.toString()+col.toString()
                        //alert(id)
                        // Add dots to the squares representing possible moves
                        var element = document.getElementById(id);
                        element.classList.add("clicked-square");
                    }
                }else{ // actually moving (normal moves)
                    $('.clicked-square').removeClass('clicked-square');
                    let pR = 8 - parseInt(response[2])
                    let pC = parseInt(response[3]) + 1
                    let row = 8 - parseInt(response[5])
                    let col = parseInt(response[6]) + 1
                    let pId = pR.toString() + pC.toString()
                    let id = row.toString() + col.toString()
                    var imageElement = $("#" + pId).find('img');
                    $('#' + pId).empty();
                    $('#' + id).empty();
                    $('#' + id).append(imageElement);
                }
            }
        });
    });
});


