import {test} from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {schedule,Trial,practiceOutcome,checkComprehension,eventTimeStatus,skipTask} from "./core.mjs";
const m=JSON.parse(readFileSync(process.env.ANX_DEMO_MANIFEST,"utf8"));
test("Python manifest and mutation rejection",()=>{
 const rows=schedule(m);assert.equal(rows.length,336);
 const bad=structuredClone(m);bad.switching[0].correct_key^=1;
 assert.throws(()=>schedule(bad));
 const wrong=structuredClone(m);wrong.decisions[0].variance_difference=0;
 assert.throws(()=>schedule(wrong));
 const v=structuredClone(m);v.mode="research";assert.throws(()=>schedule(v));
});
test("reaction time and duplicate response",()=>{
 const row=m.switching[0], t=new Trial(row);t.cue();
 assert.equal(t.answer("left",5),null);t.show(100);
 assert.equal(t.answer("left",99),null);
 const result=t.answer(row.correct_key?"right":"left",350);
 assert.equal(result.rt_ms,250);assert.equal(result.correct,true);
 assert.equal(t.answer("left",400),null);assert.equal(t.expire(),null);
});
test("timeout and loss of focus",()=>{
 let t=new Trial(m.switching[0]);t.cue();t.show(100);
 assert.equal(t.answer("left",2101).timeout,true);
 t=new Trial(m.switching[0]);t.cue();const r=t.invalidate();
 assert.equal(r.focus_lost,true);assert.equal(r.rt_ms,null);assert.equal(t.invalidate(),null);
 t=new Trial(m.switching[0]);t.cue();assert.equal(t.technicalFailure().technical_error,true);
});
test("choice outcome independent of displayed side",()=>{
 const row=m.decisions[0], t=new Trial(row);t.show(0);
 assert.equal(t.expire(),null);
 const r=t.answer(row.target_side,5000);
 assert.equal(r.target_chosen,true);assert.equal(r.correct,null);
});

test("practice gate and comprehension",()=>{
 const rows=Array.from({length:24},(_,i)=>({correct:i<18,rt_ms:250}));
 assert.equal(practiceOutcome(rows,1).passed,true);
 rows[0].rt_ms=100;assert.equal(practiceOutcome(rows,1).retry,true);
 assert.equal(practiceOutcome(rows,2).retry,false);
 assert.throws(()=>practiceOutcome(rows.slice(1),1));
 assert.equal(checkComprehension(["known","unknown","higher"]),true);
 assert.equal(checkComprehension(["known","known","higher"]),false);
 const bad=structuredClone(m);bad.practice[1][0].mapping[0]^=1;assert.throws(()=>schedule(bad));
});

test("deadline and clock validation",()=>{
 const a=new Trial(m.switching[0]);a.show(100);assert.equal(a.answer("left",2100).timeout,false);
 const b=new Trial(m.switching[0]);b.show(100);assert.equal(b.answer("left",2100.01).timeout,true);
 assert.equal(eventTimeStatus(99,101,100),"early");
 assert.equal(eventTimeStatus(120,130,100),"valid");
 assert.equal(eventTimeStatus(120,180,100),"invalid");
 assert.equal(eventTimeStatus(Date.now(),130,100),"invalid");
});
test("task skips and decision order",()=>{
 const rows=schedule(m), first=skipTask(rows,0);
 assert.equal(first.skipped.length,m.task_order[0]==="switching"?240:96);
 assert.equal(skipTask(rows,first.end).end,336);
 const wrong=structuredClone(m);wrong.decision_order.reverse();assert.throws(()=>schedule(wrong));
});
