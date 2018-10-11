const fs = require('fs')
const http = require('http')
const util = require("util")

web_pages = ["www.google.com","www.ask.com","www.dawnnews.tv","www.facebook.com","www.geo.tv","www.live.com","www.netflix","www.urdupoint.com","www.zemtv.com"] // fix hardcode

// Promises
const readFile = util.promisify(fs.readFile);

let current_directory =  process.cwd()

const decide_which_page_to_serve = (mem)=>{
    if (mem == 0.25){
        // serve low end page
        return "0.96_index.html"
    }else if(mem == 0.5){
        // serve medium end page
        return "16.32_index.html"

    }else if(mem == 1){
        // serve ~ normal page
        return "47.04_index.html"
    }else if(mem == 2){
        // serve base page
        return "108.48_index.html"
    }else{
        // for now serve base page
        return "index.html"
    }

}

const main = async ()=>{
    console.log("Starting the server")
    const server = http.createServer(async (req,resp) => {
        let response_string = "If you are seeing this string"
        x = req.rawHeaders
        try{
            if (x.indexOf("Device-Memory") == -1){
                // serve the stub page
                console.log("Serving the stub page")
                response_string = await readFile("stub.html", "utf-8")    
            }else{
                device_mem_size = x[x.indexOf("Device-Memory")+1]
                //device_mem_size = 0.25
                console.log("Device is memory size is :" + device_mem_size + "GB")
                if(req.url.search(/index.html/) == -1){
                    // normal request
                    response_string = await readFile(req.url.substr(1))
                }else{
                    // device aware response
                    request = req.url.replace("index.html", decide_which_page_to_serve(device_mem_size))
                    response_string = await readFile(request.substr(1))
                }
            }
        }catch(err){
            response_string = "file not found"
        }
        resp.end(response_string)
    })

    server.listen(12000, ()=> console.log('Listening'))
}


main()