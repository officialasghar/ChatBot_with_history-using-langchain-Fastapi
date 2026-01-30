const API_BASE = 'http://localhost:8000';

async function postJSON(path, data){
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(data)
  });
  return res.json();
}

function showMsg(el, text, isError=false){
  el.textContent = text;
  el.style.color = isError ? '#b91c1c' : '';
}

document.addEventListener('DOMContentLoaded', ()=>{
  const signupForm = document.getElementById('signup-form');
  const loginForm = document.getElementById('login-form');
  const chatForm = document.getElementById('chat-form');
  const logoutBtn = document.getElementById('logout');

  if(signupForm){
    signupForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(signupForm);
      const payload = {username: fd.get('username'), password: fd.get('password')};
      const msgEl = signupForm.querySelector('#message');
      try{
        const data = await postJSON('/signup', payload);
        showMsg(msgEl, data.message || JSON.stringify(data), !data.success);
        if(data.success){
          // suggest to login
          setTimeout(()=>{ window.location.href = 'login.html'; }, 1000);
        }
      }catch(err){ showMsg(msgEl, err.message || String(err), true); }
    });
  }

  if(loginForm){
    loginForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(loginForm);
      const payload = {username: fd.get('username'), password: fd.get('password')};
      const msgEl = loginForm.querySelector('#message');
      try{
        const data = await postJSON('/login', payload);
        showMsg(msgEl, data.message || JSON.stringify(data), !data.success);
        if(data.success && data.user_id){
          localStorage.setItem('user_id', String(data.user_id));
          setTimeout(()=>{ window.location.href = 'chat.html'; }, 600);
        }
      }catch(err){ showMsg(msgEl, err.message || String(err), true); }
    });
  }

  if(chatForm){
    const messages = document.getElementById('messages');
    const msgEl = document.getElementById('message');
    const welcomeMsg = document.getElementById('welcome-msg');
    const stored = localStorage.getItem('user_id');
    if(!stored){
      showMsg(msgEl, 'Not logged in. Please log in first.', true);
      return;
    }

    if(logoutBtn){
      logoutBtn.addEventListener('click', ()=>{ localStorage.removeItem('user_id'); window.location.href='login.html'; });
    }

    chatForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      if(welcomeMsg && welcomeMsg.parentNode) welcomeMsg.remove();
      const qInput = document.getElementById('query');
      const query = qInput.value.trim();
      if(!query) return;
      appendMessage('user', query);
      qInput.value = '';
      showMsg(msgEl, '');
      try{
        const payload = {user_id: Number(stored), query};
        const data = await postJSON('/chat', payload);
        const resp = data.Response;
        appendMessage('bot', typeof resp === 'string' ? resp : JSON.stringify(resp));
      }catch(err){ showMsg(msgEl, err.message || String(err), true); }
    });

    function appendMessage(kind, text){
      const d = document.createElement('div');
      d.className = 'msg ' + (kind === 'user' ? 'user' : 'bot');
      d.textContent = text;
      messages.appendChild(d);
      messages.scrollTop = messages.scrollHeight;
    }
  }
});
