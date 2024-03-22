import { Observable, lastValueFrom } from "rxjs";
import { LastValueFromConfig } from "rxjs/internal/lastValueFrom";

export async function performRequest(requestFunc:Observable<any>, options?:LastValueFromConfig<any>){
    let res!:any, config!:any;
    if(options && Object.keys(options).length){
        config = options;
    }
    try{
        if(config){
            res = await lastValueFrom(requestFunc, config);
        }
        else{
            res = await lastValueFrom(requestFunc)
        }
    }catch(e){
        res = e;
    }
    return res
}


