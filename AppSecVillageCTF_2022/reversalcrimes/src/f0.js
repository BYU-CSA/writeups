const m = {};
const input = document.getElementById('input');
const answer = document.getElementById('answer');

const txt = '';
answer.innerHTML = txt;
input.addEventListener('input', e =>{
  const handler = o => {
    if (o.status) {
      answer.classList.add('green');
      answer.innerHTML = `That is correct!`;
    } else {
      answer.classList.add('red');
      answer.innerText = `That is incorrect!`;
      
      setTimeout(()=>{
        answer.classList = '';
        answer.innerHTML = txt;
      }, 100);
    }
  };
  
  if (!m[0](e.target.value, handler)) {
    handler({status: false});
  }
});