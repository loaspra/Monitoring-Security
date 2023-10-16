const express = require('express');
const {Client} = require('pg');
const path = require('path');
const axios = require('axios');
const PORT = 8000;
const PORT2 = 8001;
const PORT3 = 8002;
const PORT4= 8003;
const app = express();

app.use('/images',express.static('archive/images'));
app.use(express.json());

// const db_data = {
//     user : "postgres",
//     password : "Softjuandius_25",
//     database : "postgres",
//     port : 5432
// }

// const client = new Client(db_data);

// client.connect();
async function searchApi(req,res){
    try{
        let pokemon = req.query.pokemon;
        const response_pokeapi = await axios.get(`http://localhost:8001/pokeapi?pokemon=${pokemon}`);
        console.log(response_pokeapi.data[0]);
        pokemon = pokemon.charAt(0).toUpperCase() + pokemon.slice(1); // console.log(pokemon);
        const response_poke_stats = await axios.get(`http://localhost:8002/pokestats?pokemon=${pokemon}`);
        console.log(response_poke_stats.data[0]);
        const response_poke_image = await axios.get(`http://localhost:8003/pokeImages?pokemon=${pokemon}`)
        console.log(response_poke_image.data);
        const response  ={
            pokeApi : response_pokeapi.data,
            pokeStats : response_poke_stats.data,
            pokeImage : response_poke_image.data
        }
        res.json(response);
    }catch(err){
        console.log(err.message);
    } finally {
        res.end();
    }
}

async function pokeStats(req,res){
    try{
        const pokemon = req.query.pokemon;
        // const response_pokeapi = await client.query(`select * from pokemones where name = '${pokemon}'`);
        // console.log(response_pokeapi.rows);
        // res.send(response_pokeapi.rows);
        res.send("Perro");

    }catch(err){
        console.log(err.message);
    } finally {
        res.end();
    }
}
async function pokeImages(req,res){
    try{
        console.log("aqui");
        let pokemon = req.query.pokemon;
        pokemon = pokemon.charAt(0).toUpperCase() + pokemon.slice(1);
        const image_url = path.join(__dirname,'archive/images',pokemon,'0.jpg');
        // console.log(image_url);
        res.send(image_url);
    }catch(err){
        console.log(err.message);
    } finally {
        res.end();
    }
}
async function pokeApi(req,res){
    try{
        const pokemon = req.query.pokemon;
        const response_query = await axios.get(`https://pokeapi.co/api/v2/pokemon/${pokemon}`);
        // console.log(response_query.data.forms);
        res.send(response_query.data.forms);
    } catch(err){
        console.log(err);
    } finally {
        res.end();
    }
}

app.get('/searchapi',searchApi);
app.get('/pokeapi',pokeApi);
app.get('/pokestats',pokeStats);
app.get('/pokeImages',pokeImages)
app.get('/',(req,res)=>{
    res.send("hola");
})
app.listen(PORT,(req,res)=>{
    console.log(`Escuchando puerto ${PORT}`)
})
app.listen(PORT2,(req,res)=>{
    console.log(`Escuchando puerto ${PORT2}`)
})
app.listen(PORT3,(req,res)=>{
    console.log(`Escuchando puerto ${PORT3}`)
})
app.listen(PORT4,(req,res)=>{
    console.log(`Escuchando puerto ${PORT4}`)
})