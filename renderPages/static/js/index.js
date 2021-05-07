async function callClick(){
  let response = await fetch('http://localhost:8000/click/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("data").innerHTML = answer;
}

async function getUser(id){
  let response = await fetch('http://localhost:8000/users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer['username'];
  let getCycle = await fetch('http://localhost:8000/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];
  if (cycle['boost'].length > 0){
    let getBoost = await fetch('http://localhost:8000/boosts/' + cycle['boost'][0],{
    method: 'GET'
    });
    let dataBoost = await getBoost.json();
    if (dataBoost['level'] > 0) {
      document.getElementById("level").innerHTML = dataBoost['level'];
      document.getElementById("price").innerHTML = dataBoost['price'];
    } 
  }
}

async function buyBoost(id){
  let response = await fetch('http://localhost:8000/users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();
  let getCycle = await fetch('http://localhost:8000/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  if (cycle['boost'].length > 0){
    let getBoost = await fetch('http://localhost:8000/boosts/' + cycle['boost'][0],{
    method: 'GET'
    });
    let dataBoost = await getBoost.json();
    if (dataBoost['level'] > 0) {
      let buyBoost = await fetch('http://localhost:8000/upgradeBoost/',{
      method: 'GET'
      });
      let answer = await buyBoost.json();
      document.getElementById("clickPower").innerHTML = answer; 
    } 
  }
  else {
    let buyBoost = await fetch('http://localhost:8000/buyBoost/',{
    method: 'GET'
    });
    let answer = await buyBoost.json();
    document.getElementById("clickPower").innerHTML = answer;
  }

  let updateCycle = await fetch('http://localhost:8000/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let newCycle = await updateCycle.json();
  document.getElementById("data").innerHTML = newCycle['coinsCount'];
  let updateBoost = await fetch('http://localhost:8000/boosts/' + newCycle['boost'][0],{
    method: 'GET'
    });
  let newBoost = await updateBoost.json();
  document.getElementById("level").innerHTML = newBoost['level'];
  document.getElementById("price").innerHTML = newBoost['price'];
}



