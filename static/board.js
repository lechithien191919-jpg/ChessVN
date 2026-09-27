const ICON={P:'♙',N:'♘',B:'♗',R:'♖',Q:'♕',K:'♔',p:'♟',n:'♞',b:'♝',r:'♜',q:'♛',k:'♚'};
let board, turn, selected=null, history=[], castle, ep, pendingPromo=null, lastMove=null, thinking=false;

function initialBoard(){
  return [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
  ];
}

function resetGame(){
  board = initialBoard();
  turn = 'w';
  selected = null;
  history = [];
  castle = {K:true, Q:true, k:true, q:true};
  ep = null;
  pendingPromo = null;
  lastMove = null;
  thinking = false;
  document.getElementById('promo').style.display = 'none';
  render();
}

function clone(b){ return b.map(r => r.slice()); }

function render(){
  const el = document.getElementById('board');
  el.innerHTML = '';
  for(let r=0; r<8; r++){
    for(let c=0; c<8; c++){
      let sq = document.createElement('div');
      sq.className = 'sq ' + ((r+c)%2 ? 'dark' : 'light');
      if(selected && selected[0]===r && selected[1]===c) sq.classList.add('selected');
      if(lastMove && ((lastMove[0]===r && lastMove[1]===c) || (lastMove[2]===r && lastMove[3]===c))) sq.classList.add('last');
      
      if(board[r][c]){
        let sp = document.createElement('span');
        sp.className = 'piece ' + (board[r][c] === board[r][c].toUpperCase() ? 'whitePiece' : 'blackPiece');
        sp.textContent = ICON[board[r][c]];
        sq.appendChild(sp);
      }
      sq.onclick = () => clickSq(r, c);
      el.appendChild(sq);
    }
  }
  document.getElementById('status').textContent = thinking ? '🤖 Máy đang suy nghĩ...' : (turn === 'w' ? '⚪ Lượt của bạn (Chọn quân Trắng để đi)' : '⚫ Lượt của máy');
}

function clickSq(r, c){
  if(thinking || turn !== 'w') return;
  if(selected){
    if(selected[0] === r && selected[1] === c){ selected = null; render(); return; }
    humanMove(selected[0], selected[1], r, c);
    return;
  }
  if(board[r][c] && board[r][c] === board[r][c].toUpperCase()){
    selected = [r, c];
    render();
  }
}

function humanMove(r, c, rr, cc){
  let p = board[r][c];
  if(p === 'P' && rr === 0){
    pendingPromo = {r, c, rr, cc};
    document.getElementById('promo').style.display = 'flex';
    return;
  }
  commitMove(r, c, rr, cc, null);
}

document.querySelectorAll('#promos button').forEach((btn, idx) => {
  let pieces = ['Q', 'R', 'B', 'N'];
  btn.onclick = () => {
    document.getElementById('promo').style.display = 'none';
    let x = pendingPromo;
    pendingPromo = null;
    commitMove(x.r, x.c, x.rr, x.cc, pieces[idx]);
  };
});

function commitMove(r, c, rr, cc, promo){
  history.push({board: clone(board), castle: {...castle}, ep: ep ? [...ep] : null, turn});
  let p = board[r][c];
  board[r][c] = null;
  board[rr][cc] = promo ? promo : p;
  
  lastMove = [r, c, rr, cc];
  selected = null;
  turn = 'b';
  render();

  thinking = true;
  render();

  fetch('/get_ai_move', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board, level: document.getElementById('level').value, castle, ep})
  })
  .then(res => res.json())
  .then(res => {
    thinking = false;
    if(res && res.from && res.to){
      let fr = res.from, to = res.to;
      let ap = board[fr[0]][fr[1]];
      board[fr[0]][fr[1]] = null;
      board[to[0]][to[1]] = res.promo ? res.promo : ap;
      lastMove = [fr[0], fr[1], to[0], to[1]];
    }
    turn = 'w';
    render();
  }).catch(err => {
    thinking = false;
    turn = 'w';
    render();
  });
}

document.getElementById('new').onclick = resetGame;
document.getElementById('undo').onclick = () => {
  if(!history.length || thinking) return;
  let last = history.pop();
  board = last.board;
  castle = last.castle;
  ep = last.ep;
  turn = last.turn;
  selected = null;
  lastMove = null;
  render();
};

resetGame();
        
