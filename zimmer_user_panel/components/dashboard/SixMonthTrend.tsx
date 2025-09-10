"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card, Skeleton } from "@/components/ui/Kit";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";

type Row = { month:string; value:number };

export default function SixMonthTrend(){
  const [data,setData]=useState<Row[]|null>(null);
  const [err,setErr]=useState<string|null>(null);
  useEffect(()=>{(async()=>{
    try{
      const r=await apiFetch("/api/user/usage?range=6m");
      if(!r.ok) throw new Error();
      setData(await r.json());
    }catch{ 
      setErr("خطا در دریافت آمار شش ماه اخیر");
    }
  })()},[]);
  return (
    <Card className="col-span-12 lg:col-span-7">
      <div className="font-semibold mb-3">آمار شش ماه اخیر</div>
      {!data && !err && <Skeleton className="h-56" />}
      {err && <div className="text-sm text-red-600">{err}</div>}
      {data && (
        <motion.div initial={{opacity:0}} animate={{opacity:1}}>
          <div style={{width:"100%", height:220}}>
            <ResponsiveContainer>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#8B5CF6" strokeWidth={2} dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}
    </Card>
  );
}
