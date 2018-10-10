const fs = require('fs')
const http = require('http')
const util = require("util")

web_pages = ["www.google.com","www.ask.com","www.dawnnews.tv","www.facebook.com","www.geo.tv","www.live.com","www.netflix","www.urdupoint.com","www.zemtv.com"] // fix hardcode

// Promises
const readFile = util.promisify(fs.readFile);

let current_directory =  process.cwd()
let temp_mem_available =  2048 // 2 GB

const decide_which_page_to_serve = (mem)=>{
    if (mem == 512){
        // serve low end page
        return "low_index.html"
    }else if(mem == 1024){
        // serve medium end page
        return "mid_index.html"

    }else if(mem == 2048){
        // serve ~ normal page
        return "high_index.html"
    }else if(mem == 4096){
        // serve base page
        return "base_index.html"
    }else{
        // for now serve base page
        return "index.html"
    }

}

const main = async ()=>{
    console.log("Starting the server")
    const server = http.createServer(async (req,resp) => {
        let response_string = "If you are seeing this string"
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