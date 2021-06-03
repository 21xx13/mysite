async function callClick(){
  let response = await fetch('/click/',{
    method: 'GET'
  });
  let answer = await response.json();
  
  const coins_counter = document.getElementById('data').innerText;
  let coins_value = parseInt(coins_counter);
  let level_counter = parseInt(document.getElementById('player-level').innerText) - 1;
  if (coins_value > (level_counter**2+1)*1000) {
    level_counter += 1
    document.getElementById('player-level').innerHTML = level_counter + 1;
  }
  const click_power = document.getElementById('clickPower').innerText;
  coins_value += parseInt(click_power);
  document.getElementById("data").innerHTML = coins_value;

  if(answer.boosts){
    saved_boosts = answer.boosts;
    renderBoosts(answer.boosts);
  }
}

let saved_boosts;
let boosts_front = [["Коробка печенья", "Съев печенье, енот станет чуть сильнее.", "https://vk.com/doc137795470_597854008?hash=becb780aef1be74541&dl=d4fb09b057e04fbe4b&wnd=1"],
["Бахни кофейку!", "Енот станет еще активнее.", "https://vk.com/doc137795470_597854007?hash=41c0f71bb08c57b093&dl=73df282e2baf4cd15b&wnd=1"], 
["Мусорка", "Можно найти много чего интересного! Или просто немного расслабиться.", "https://vk.com/doc137795470_597929563?hash=f06b7fedd0bdd2e291&dl=69746d1177d09fc944&wnd=1"], 
["Напугать соседей", "Надоела громкая музыка или просто стало скучно? Самое время напугать надоедливых соседей!", "https://vk.com/doc137795470_597929581?hash=0d0a0709084189bdf2&dl=b299355424cf624c83&wnd=1"], 
["Захватить мир", "Мечты о захвате мира взбодрят енота.", "https://vk.com/doc137795470_597929579?hash=f218a03fdb13df662c&dl=fb8f6344f7a933bebf&wnd=1"], 
["Поработать", "Не всё же время отдыхать! Пора немного потрудиться.", "https://vk.com/doc137795470_597929560?hash=19ab63174d1ce6c77f&dl=18a359fb990c79d580&wnd=1"]];
let isAutoClickOn = false;

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
  saved_boosts = boosts;
  set_auto_click();
  set_send_coins_interval();
  isAutoClickOn = true;
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
    document.getElementById("autoClickPower").innerHTML = data['autoClickPower'];
    document.getElementById("data").innerHTML = data['coinsCount'];
    if (!isAutoClickOn && data['autoClickPower'] > 0){
      set_auto_click();
      set_send_coins_interval();
      isAutoClickOn = true;
    }
    renderBoosts(data['boosts']);
    saved_boosts = data['boosts'];
  })
}

function set_auto_click() {
  setInterval(async function() {
      const coins_counter = document.getElementById('data').innerText;
      let coins_value = parseInt(coins_counter);
      let level_counter = parseInt(document.getElementById('player-level').innerText) - 1;
      if (coins_value > (level_counter**2+1)*1000) {
        level_counter += 1
        document.getElementById('player-level').innerHTML = level_counter + 1;
      }
      const auto_click_power = document.getElementById('autoClickPower').innerText;
      coins_value += parseInt(auto_click_power);
      document.getElementById("data").innerHTML = coins_value;
      renderBoosts(saved_boosts);    
  }, 1000)
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
  let autoClickName = boost.boost_type == 1 ? "" : " (Автоклик)";
  let autoClickPower = boost.boost_type == 1 ? "" : "авто";
  let methodBuy = `onclick="buyBoost(${boost.level})"`;
  const li = document.createElement('li');
  li.setAttribute('class', 'boost-item');
  if (boost.boost_type == 0)
    li.setAttribute('class', 'autoClick');
  if (+document.getElementById("data").innerHTML < boost.price){
    li.setAttribute('class', 'disabled');
    methodBuy = "";
  }
   
  
  li.setAttribute('id', `boost-item-${boost.level}`);
  li.innerHTML = `
    <div class="wrapper-item">
      <div class="boost-name"><strong>${boosts_front[boost.level % boosts_front.length][0]}` + autoClickName + `</strong></div>
      <div class="boost-description">${boosts_front[boost.level % boosts_front.length][1]} +<span id="power_${boost.level}">${boost.power}</span> к силе ` 
      + autoClickPower +`клика.</div>
      <div class="boost-description">Текущий уровень: <span id="level_${boost.level}">${boost.level_boost}</span></div>
      <div class="boost-cost">Цена: <span id="price_${boost.level}">${boost.price}</span></div>
      </div>
      <input type="image"  src="${boosts_front[boost.level % boosts_front.length][2]}"` + methodBuy +  ` height="150""/>
  `;
  parent.appendChild(li);
 }

 function set_send_coins_interval() {
  setInterval(function() {
      const csrftoken = getCookie('csrftoken');
      const coins_counter = document.getElementById('data').innerText;
      fetch('/set_maincycle/', {
          method: 'POST',
          headers: {
              "X-CSRFToken": csrftoken,
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              coinsCount: coins_counter,
          })
      }).then(response => {
          if (response.ok) {
              return response.json()
          } else {
              return Promise.reject(response)
          }
      }).then(data => {
          console.log('Coins  count sended to server');
      }).catch(err => console.log(err))
  }, 10000)
}

