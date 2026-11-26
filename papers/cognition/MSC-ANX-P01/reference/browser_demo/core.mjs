/* Pure demonstration state and schedule validation. */
export const TIMING = Object.freeze({cue_ms:300,response_ms:2000,iti_ms:500});
const NUMBERS=[1,2,3,4,6,7,8,9];
const fail=()=>{throw new Error("Nieprawidłowy manifest demonstracyjny.");};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const cat=(rule,n)=>rule===0?n%2:Number(n>5);
const integer=(n)=>Number.isSafeInteger(n);
const finite=(n)=>typeof n==="number"&&Number.isFinite(n);

export function schedule(m) {
  if(!m || m.mode!=="local-demo" || m.demo_version!=="0.2.0" || m.protocol_version!=="0.4.0" ||
      m.stimulus_version!=="0.4.1" || !integer(m.seed) || m.seed<0 ||
      !m.timing || Object.keys(TIMING).some(k=>m.timing[k]!==TIMING[k]) ||
      ![["switching","decision"],["decision","switching"]].some(x=>same(x,m.task_order)) ||
      !Array.isArray(m.switching)||m.switching.length!==240 ||
      !Array.isArray(m.decisions)||m.decisions.length!==96) fail();
  let i=0, mapping=null, counts={switch:0,repeat:0}, repeats={switch:0,repeat:0};
  for(let b=0;b<6;b++){
    let previous=null;
    for(let t=0;t<(b<2?24:48);t++,i++){
      const row=m.switching[i];
      if(!row||row.task!=="switching"||row.block!==b||row.trial_index!==t||
        row.mixed!==(b>=2)||![0,1].includes(row.rule)||!NUMBERS.includes(row.stimulus)||
        !integer(row.cue)||Math.floor(row.cue/2)!==row.rule||
        !Array.isArray(row.mapping)||row.mapping.length!==2||row.mapping.some(x=>![0,1].includes(x))||
        row.correct_key!==(cat(row.rule,row.stimulus)^row.mapping[row.rule]))fail();
      if(mapping===null)mapping=row.mapping;
      if(!same(mapping,row.mapping))fail();
      const transition=previous?(previous.rule===row.rule?"repeat":"switch"):"undefined";
      if(row.transition!==transition||(previous&&row.cue===previous.cue)||(b<2&&transition==="switch"))fail();
      if(b>=2&&previous){counts[transition]++;repeats[transition]+=Number(previous.stimulus===row.stimulus);}
      previous=row;
    }
  }
  if(counts.switch!==94||counts.repeat!==94||repeats.switch!==12||repeats.repeat!==12)fail();
  if(!Array.isArray(m.practice)||m.practice.length!==2)fail();
  for(const [a,block] of m.practice.entries()){
    if(!Array.isArray(block)||block.length!==24)fail();
    let prev=null;
    for(const [t,row] of block.entries()){
      if(!row||row.practice!==true||row.practice_attempt!==a+1||row.task!=="switching"||
        row.block!==2||row.trial_index!==t||row.mixed!==true||![0,1].includes(row.rule)||
        !NUMBERS.includes(row.stimulus)||!integer(row.cue)||Math.floor(row.cue/2)!==row.rule||
        !same(row.mapping,mapping)||row.correct_key!==(cat(row.rule,row.stimulus)^mapping[row.rule])||
        row.transition!==(prev?(prev.rule===row.rule?"repeat":"switch"):"undefined")||
        (prev&&row.cue===prev.cue))fail();
      prev=row;
    }
  }
  for(const [j,task] of ["risk","ambiguity"].entries()){
    const cells=new Map();
    for(let t=0;t<48;t++){
      const row=m.decisions[j*48+t];
      if(!row||row.task!==task||row.block!==0||row.trial_index!==t||
        !["left","right"].includes(row.target_side)||![-2,0,2].includes(row.contrast)||
        ![0,1,2,3].includes(row.level)||row.reference_p!==.5)fail();
      const d=row.contrast,l=row.level;
      if(task==="risk"){
        const s=l+3;
        if(!same(row.reference_outcomes,[10,14])||!same(row.target_outcomes,[12+d-s,12+d+s])||
          row.target_p!==.5||row.ev_difference!==d||row.variance_difference!==s*s-4)fail();
      }else{
        const w=(l+1)/10;
        if(!same(row.reference_outcomes,[8,16])||!same(row.target_outcomes,[8+d,16+d])||
          row.target_p!==null||!same(row.ambiguity_bounds,[Number((.5-w).toFixed(2)),Number((.5+w).toFixed(2))])||
          row.nominal_payoff_contrast!==d||row.ambiguity_width!==Number((2*w).toFixed(2)))fail();
      }
      const k=[d,l,row.target_side].join("/");
      cells.set(k,(cells.get(k)||0)+1);
    }
    if(cells.size!==24||[...cells.values()].some(n=>n!==2))fail();
  }
  return m.task_order.flatMap(task=>task==="switching"?m.switching:m.decisions);
}

export class Trial {
  constructor(row){
    this.row=row; this.phase="ready"; this.onset=null; this.result=null;
  }
  cue(){if(this.phase!=="ready")throw new Error("phase"); this.phase="cue";}
  show(at){if(!["ready","cue"].includes(this.phase)||!finite(at))throw new Error("phase/time");this.onset=at;this.phase="response";}
  finish(fields){
    if(this.result)return null;
    this.phase="done";
    this.result={...this.row,rt_ms:null,response:null,correct:null,target_chosen:null,
      timeout:false,focus_lost:false,technical_error:false,...fields};
    return this.result;
  }
  answer(side,at){
    if(this.phase!=="response"||!["left","right"].includes(side)||!finite(at)||at<this.onset)return null;
    const rt=at-this.onset;
    if(this.row.task==="switching"&&rt>TIMING.response_ms)return this.expire();
    const isSwitch=this.row.task==="switching";
    return this.finish({rt_ms:rt,response:side,
      correct:isSwitch?Number(side==="right")===this.row.correct_key:null,
      target_chosen:isSwitch?null:side===this.row.target_side});
  }
  expire(){
    if(this.phase!=="response"||this.row.task!=="switching")return null;
    return this.finish({timeout:true,correct:false});
  }
  invalidate(){
    if(!["cue","response"].includes(this.phase))return null;
    return this.finish({focus_lost:true});
  }
  technicalFailure(){
    if(!["cue","response"].includes(this.phase))return null;
    return this.finish({technical_error:true});
  }
}

export function practiceOutcome(results,attempt){
  if(![1,2].includes(attempt)||results.length!==24)throw new Error("incomplete practice");
  const correct=results.filter(r=>r.correct===true&&!r.timeout&&!r.focus_lost&&!r.technical_error&&
    finite(r.rt_ms)&&r.rt_ms>=150&&r.rt_ms<=TIMING.response_ms).length;
  return {attempt,correct,total:24,passed:correct>=18,retry:correct<18&&attempt===1};
}
export function checkComprehension(answers){
  return Array.isArray(answers)&&answers.length===3&&
    answers[0]==="known"&&answers[1]==="unknown"&&answers[2]==="higher";
}
