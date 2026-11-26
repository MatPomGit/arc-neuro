import {schedule,Trial,TIMING,practiceOutcome,checkComprehension,EVENT_GRACE_MS,eventTimeStatus,skipTask} from "./core.mjs";
const $=id=>document.getElementById(id);
let manifest=null, rows=[], results=[], active=null, index=0, generation=0, running=false;
let paused=false, timer=null, stopped=false, heldKeys=new Set();
let practiceAttempt=0, practiceResults=[], practiceHistory=[], trainingPassed=false, practicing=false;
let quizPassed=false, quizAttempts=0, endReason=null, timingDiagnostics=[], skippedTrials=[];
const keys={KeyF:"left",KeyJ:"right"};
const focusOK=()=>!document.hidden&&document.hasFocus();
function clear(){generation++;clearTimeout(timer);timer=null;}
function setScreen(instruction="",cue="",stimulus="",left="",right=""){
  for(const [id,value] of Object.entries({instruction,cue,stimulus,left,right}))$(id).textContent=value;
}
function stateProgress(){
  $("progress").textContent=practicing?"Trening "+practiceAttempt+": "+Math.min(practiceResults.length+1,24)+" / 24":"Próba "+Math.min(index+1,rows.length)+" / "+rows.length;
  $("bar").value=index;
}
function guard(token){return running&&!paused&&generation===token;}
function frame(token,fn){requestAnimationFrame(()=>{if(guard(token))fn();});}
function pause(message){
  clear();paused=true;active=null;setScreen(message);$("resume").hidden=false;
}
function blockLabel(row){
  if(row.task==="switching")return "Klasyfikacja liczby. Kieruj się wskazówką i mapowaniem klawiszy.";
  if(row.task==="risk")return "Wybierz preferowaną loterię punktową. Prawdopodobieństwa są jawne.";
  return "Wybierz preferowaną loterię. W jednej z opcji prawdopodobieństwo jest znane tylko jako przedział.";
}
function next(){
  if(!running)return;
  stateProgress();
  if(index>=rows.length){finish(false);return;}
  if(!focusOK()){pause("Przywróć fokus okna i kontynuuj.");return;}
  if(heldKeys.size){pause("Zwolnij klawisze odpowiedzi i kontynuuj.");return;}
  const row=practicing?manifest.practice[practiceAttempt-1][practiceResults.length]:rows[index];
  active=new Trial(row);
  const token=++generation;
  if(row.task==="switching"){
    active.cue();
    const labels=row.rule===0?["parzysta","nieparzysta"]:["mniejsza niż 5","większa niż 5"];
    const mapping=row.mapping[row.rule];
    const cue=(row.rule===0?["PARZYSTOŚĆ","PARZYSTA / NIEPARZYSTA"]:["WIELKOŚĆ","MNIEJSZA / WIĘKSZA"])[row.cue%2];
    frame(token,()=>{
      if(!focusOK()){lostFocus();return;}
      setScreen("",cue,"","F: "+labels[mapping],"J: "+labels[1-mapping]);
      const cueAt=performance.now();
      timer=setTimeout(()=>frame(token,()=>{
        if(!focusOK()){lostFocus();return;}
        $("stimulus").textContent=String(row.stimulus);
        active.show(performance.now());
        timingDiagnostics.push({practice:practicing,block:row.block,trial_index:row.trial_index,practice_attempt:practicing?practiceAttempt:null,
          cue_to_dom_ms:active.onset-cueAt});
        if(active.onset-cueAt>TIMING.cue_ms+150){
          record(active.technicalFailure(),true);return;
        }
        // Grace period lets a queued pre-deadline key event arrive; RT still uses event time.
        timer=setTimeout(()=>{if(guard(token)){
          const lag=performance.now()-active.onset-TIMING.response_ms;
          if(lag>EVENT_GRACE_MS){record(active.technicalFailure(),true);return;}
          $("stimulus").textContent="";
          timer=setTimeout(()=>{if(guard(token)){
            const extra=performance.now()-active.onset-TIMING.response_ms-EVENT_GRACE_MS;
            record(extra>EVENT_GRACE_MS?active.technicalFailure():active.expire(),extra>EVENT_GRACE_MS);
          }},Math.max(0,TIMING.response_ms+EVENT_GRACE_MS-(performance.now()-active.onset)));
        }},TIMING.response_ms);
      }),TIMING.cue_ms);
    });
  }else{
    // Choice display has no response deadline; key responses only.
    active.cue();
    const lot=(out,p,bounds)=>out[0]+" lub "+out[1]+" pkt\nP(wyższej wypłaty): "+(p===null?bounds.map(x=>Math.round(x*100)+"%").join("–"):Math.round(p*100)+"%");
    const ref=lot(row.reference_outcomes,row.reference_p), target=lot(row.target_outcomes,row.target_p,row.ambiguity_bounds);
    frame(token,()=>{
      if(!focusOK()){lostFocus();return;}
      setScreen(blockLabel(row),"","",row.target_side==="left"?target:ref,row.target_side==="right"?target:ref);
      active.show(performance.now());
    });
  }
}
function omitCurrentTask(reason){
  const skipped=skipTask(rows,index);
  skippedTrials.push(...skipped.skipped.map(t=>({...t,reason})));
  index=skipped.end;
  if(index>=rows.length){finish(false,"completed_with_skips");return;}
  stateProgress();pause("Pominięto zadanie. "+blockLabel(rows[index]));
}
function record(result,interrupted=false){
  if(!result||!running)return;
  clear();
  if(practicing){
    practiceResults.push(result);active=null;stateProgress();
    if(practiceResults.length===24){
      const outcome=practiceOutcome(practiceResults,practiceAttempt);
      practiceHistory.push(outcome);practicing=false;practiceResults=[];
      if(outcome.passed){
        trainingPassed=true;
        pause("Trening zaliczony: "+outcome.correct+"/24. Rozpocznij próby właściwe.");
      }else if(outcome.retry){
        pause("Trening: "+outcome.correct+"/24. Wymagane 18 poprawnych. Powtórz trening.");
      }else{omitCurrentTask("practice_failed");}
      return;
    }
    if(interrupted||!focusOK()){pause("Próba treningowa nieważna. Przywróć fokus.");return;}
    setScreen(result.correct&&result.rt_ms>=150?"Poprawnie":"Niepoprawnie lub odpowiedź zbyt szybka");
    const token=generation;
    timer=setTimeout(()=>{if(guard(token))next();},TIMING.iti_ms);
    return;
  }
  results.push(result); index++; active=null;stateProgress();
  if(index>=rows.length){finish(false);return;}
  const previous=rows[index-1], upcoming=rows[index];
  if(interrupted||!focusOK()){pause("Próba nieważna. Przywróć fokus i kontynuuj.");return;}
  if(previous.task!==upcoming.task||previous.block!==upcoming.block){pause("Przerwa. "+blockLabel(upcoming));return;}
  setScreen();
  const token=generation;
  timer=setTimeout(()=>{if(guard(token))next();},TIMING.iti_ms);
}
function lostFocus(){
  heldKeys.clear();
  if(!running||paused)return;
  if(active){record(active.invalidate(),true);}
  else pause("Przywróć fokus okna i kontynuuj.");
}
function finish(manual,reason=null){
  endReason=reason||(manual?"manual_stop":skippedTrials.length?"completed_with_skips":"completed");
  stopped=manual;running=false;paused=false;clear();active=null;
  $("session").hidden=true;$("done").hidden=false;
  $("summary").textContent="Zapisano "+results.length+" z "+rows.length+" prób demonstracyjnych. "+(skippedTrials.length?" Pominięto "+skippedTrials.length+" prób.":"");
}
$("manifest").addEventListener("change",async e=>{
  manifest=null;rows=[];$("start").disabled=true;
  const file=e.target.files[0];if(!file)return;
  try{
    if(file.size>2e6)throw new Error("Manifest przekracza limit rozmiaru.");
    const candidate=JSON.parse(await file.text());
    if(e.target.files[0]!==file)return;
    const validated=schedule(candidate);
    manifest=candidate;rows=validated;
    $("status").textContent="Manifest poprawny: "+rows.length+" prób; wersja "+manifest.stimulus_version+".";
    $("start").disabled=false;
  }catch(err){$("status").textContent=String(err.message);}
});
$("start").addEventListener("click",()=>{
  if(!manifest||running)return;
  running=true;index=0;results=[];stopped=false;
  practiceAttempt=0;practiceHistory=[];practiceResults=[];trainingPassed=false;practicing=false;
  quizPassed=false;quizAttempts=0;endReason=null;timingDiagnostics=[];skippedTrials=[];$("setup").hidden=true;$("session").hidden=false;
  stateProgress();pause("Demonstracja. "+blockLabel(rows[0]));
});
$("resume").addEventListener("click",()=>{
  if(!running||!paused||!focusOK()||heldKeys.size)return;
  const row=rows[index];
  if(!practicing&&row.task==="switching"&&!trainingPassed){
    practiceAttempt++;practiceResults=[];practicing=true;
  }
  if(!practicing&&row.task!=="switching"&&!quizPassed){
    $("quiz").hidden=false;$("resume").hidden=true;return;
  }
  paused=false;$("resume").hidden=true;next();
});
$("quiz-submit").addEventListener("click",()=>{
  if(!running||!paused||quizPassed||$("quiz").hidden)return;
  quizAttempts++;
  if(!checkComprehension(["q1","q2","q3"].map(id=>$(id).value))){
    if(quizAttempts>=2){
      $("quiz").hidden=true;omitCurrentTask("comprehension_failed");return;
    }
    $("quiz-feedback").textContent="Sprawdź instrukcję: przy dokładnej wartości p prawdopodobieństwo jest określone; przedział wyznacza tylko granice. Zwróć uwagę na opis wypłaty.";
    for(const id of ["q1","q2","q3"])$(id).value="";
    return;
  }
  quizPassed=true;$("quiz").hidden=true;
  pause("Sprawdzenie rozumienia zaliczone. "+blockLabel(rows[index]));
});
$("stop").addEventListener("click",()=>finish(true));
window.addEventListener("keydown",e=>{
  if(!running||!keys[e.code])return;
  e.preventDefault();
  const blocked=e.repeat||heldKeys.size>0;
  heldKeys.add(e.code);
  if(blocked)return;
  if(!paused&&active&&focusOK()){
    const now=performance.now();
    // Event time may be relative to a different clock on older browsers.
    const stamp=e.timeStamp;
    if(active.phase==="response"){
      const status=eventTimeStatus(stamp,now,active.onset);
      if(status==="early")return;
      if(status==="invalid"){record(active.technicalFailure(),true);return;}
    }
    record(active.answer(keys[e.code],stamp));
  }
});
window.addEventListener("keyup",e=>{if(keys[e.code])heldKeys.delete(e.code);});
window.addEventListener("blur",lostFocus);
document.addEventListener("visibilitychange",()=>{if(document.hidden)lostFocus();});
$("export").addEventListener("click",()=>{
  const report={data_origin:"demonstration",mode:"local-demo",protocol_version:manifest.protocol_version,
    stimulus_version:manifest.stimulus_version,seed:manifest.seed,task_order:manifest.task_order,decision_order:manifest.decision_order,
    demo_version:manifest.demo_version,practice_history:practiceHistory,training_passed:trainingPassed,
    incomplete_practice_trials:practicing?practiceResults.length:0,
    comprehension_passed:quizPassed,comprehension_attempts:quizAttempts,end_reason:endReason,
    timing_diagnostics:timingDiagnostics,skipped_trials:skippedTrials,
    timing:TIMING,planned_trials:rows.length,completed_trials:results.length,stopped,
    trials:results,timing_note:"RAF/DOM update proxy, not measured physical display onset"};
  const url=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download="msc-anx-p01-DEMO.json";a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
});
