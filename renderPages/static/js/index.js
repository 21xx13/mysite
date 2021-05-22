async function callClick(){
  let response = await fetch('/click/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("data").innerHTML = answer['coinsCount'];
  document.getElementById("player-level").innerHTML = +answer['cycleLevel'] + 1;
  if(answer.boosts){
    renderBoosts(answer.boosts);
  }
}

let boosts_front = [["Коробка печенья", "Съев печенье, енот станет чуть сильнее.", "https://vk.com/doc137795470_597854008?hash=becb780aef1be74541&dl=d4fb09b057e04fbe4b&wnd=1"],
["Бахни кофейку!", "Енот станет еще активнее.", "https://vk.com/doc137795470_597854007?hash=41c0f71bb08c57b093&dl=73df282e2baf4cd15b&wnd=1"], 
["Мусорка", "Можно найти много чего интересного! Или просто немного расслабиться.", "https://vk.com/doc137795470_597929563?hash=f06b7fedd0bdd2e291&dl=69746d1177d09fc944&wnd=1"], 
["Напугать соседей", "Надоела громкая музыка или просто стало скучно? Самое время напугать надоедливых соседей!", "https://vk.com/doc137795470_597929581?hash=0d0a0709084189bdf2&dl=b299355424cf624c83&wnd=1"], 
["Захватить мир", "Мечты о захвате мира взбодрят енота.", "https://vk.com/doc137795470_597929579?hash=f218a03fdb13df662c&dl=fb8f6344f7a933bebf&wnd=1"], 
["Поработать", "Не всё же время отдыхать! Пора немного потрудиться.", "https://vk.com/doc137795470_597929560?hash=19ab63174d1ce6c77f&dl=18a359fb990c79d580&wnd=1"]];

async function getUser(id){
  let response = await fetch('/users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer['username'];
  let getCycle = await fetch('/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];
  document.getElementById("player-level").innerHTML = 1 + +cycle['level'];
  let boost_request = await fetch('/boosts/' + answer.cycle, {
    method :'GET'
  })
  let boosts = await boost_request.json();
  renderBoosts(boosts);
}

function buyBoost(boost_level){
  const csrftoken = getCookie('csrftoken')

    fetch('/buyBoost/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            boost_level: boost_level
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return Promise.reject(response)
        }
    }).then(data => {
    document.getElementById(`clickPower`).innerHTML = data['clickPower'];
    document.getElementById("data").innerHTML = data['coinsCount'];
    renderBoosts(data['boosts']);
  })
}

function getCookie(name){
  let cookieValue = null;
  if (document.cookie && document.cookie !== ''){
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++){
      const cookie = cookies[i].trim();
      if(cookie.substring(0, name.length +1) === (name + '=')){
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function renderBoosts(boosts){
  let parent = document.getElementById('boost-wrapper');
  parent.innerHTML ='';
  boosts.forEach(boost => {
    renderBoost(parent, boost)
  });
}

function renderBoost(parent, boost){

  const li = document.createElement('li');
  li.setAttribute('class', 'boost-item');
  if (+document.getElementById("data").innerHTML < boost.price)
    li.setAttribute('class', 'disabled');
  li.setAttribute('id', `boost-item-${boost.level}`);
  li.innerHTML = `
    <div class="wrapper-item">
      <div class="boost-name"><strong>${boosts_front[boost.level % boosts_front.length][0]}</strong></div>
      <div class="boost-description">${boosts_front[boost.level % boosts_front.length][1]} +<span id="power_${boost.level}">${boost.power}</span> к силе клика.</div>
      <div class="boost-description">Текущий уровень: <span id="level_${boost.level}">${boost.level_boost}</span></div>
      <div class="boost-cost">Цена: <span id="price_${boost.level}">${boost.price}</span></div>
      </div>
      <input type="image"  src="${boosts_front[boost.level % boosts_front.length][2]}" onclick="buyBoost(${boost.level})" height="150""/>
  `;
  parent.appendChild(li);
 }

