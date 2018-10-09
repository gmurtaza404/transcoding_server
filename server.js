const fs = require('fs')
const http = require('http')
const util = require("util")

web_pages = ["www.google.com","www.ask.com","www.dawnnews.tv","www.facebook.com","www.geo.tv","www.live.com","www.netflix","www.urdupoint.com","www.zemtv.com"]

// Promises
const readFile = util.promisify(fs.readFile);

let current_directory =  process.cwd()










const main = async ()=>{
    console.log("Starting the server")
    const server = http.createServer(async (req,resp) => {
        let response_string = "abc"
        console.log(req.url)
        try {
            response_string = await readFile(req.url.substr(1))
            
        }catch(err){
            response_string = "file not found"
        }
        resp.end(response_string)
    })

    server.listen(12000, ()=> console.log('Listening'))
}


main()