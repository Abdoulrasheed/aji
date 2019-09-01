/*

API Expected quiery result:
  {
    "q": [
      {
        "id": 1,
        "v_type": "Napep",
        "amount": 2000,
        "date": "2019-09-01T05:05:27.566Z",
        "gate": "Gate 1",
        "user_id": 1
      },
      {
        "id": 2,
        "v_type": "Car",
        "amount": 500,
        "date": "2019-09-01T05:05:47.400Z",
        "gate": "Gate 3",
        "user_id": 1
      },
      {
        "id": 3,
        "v_type": "Car",
        "amount": 300,
        "date": "2019-09-01T05:06:06.308Z",
        "gate": "Gate 2",
        "user_id": 1
      }
    ],
    "total": 2800
  }



But instead ()
*/




















const url = 'https://ghfod4drnbgjvg55tv6dtkwqiu.appsync-api.us-east-2.amazonaws.com/graphql'
const apikey = 'da2-vrrid7kj2vhovlv6fnjecpma6q'
const region = 'us-east-2'

// var opts = {
//   method: "GET",
//   headers: { "key": apikey },
//   body: JSON.stringify({ query: mutation })
// };

// console.log(`opts ${opts}`)


/*const query = `
  query {
    Lift(id: "panorama") {
      name
      status
    }
  }
`;
const url = "https://snowtooth.moonhighway.com/";
const opts = {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query })
};
fetch(url, opts)
  .then(res => res.json())
  .then(console.log)
  .catch(console.error);*/