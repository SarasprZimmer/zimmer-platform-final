"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card, Skeleton } from "@/components/Skeleton";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";
import { mockData } from "@/lib/mockApi";

type Row = { month:string; value:number };

export default function SixMonthTrend(){
  const [data,setData]=useState<Row[]|null>(null);
  const [err,setErr]=useState<string|null>(null);
  useEffect(()=>{(async()=>{
    try{
      // Always use mock data for now since API endpoints are not ready
      console.log('Using mock data for six month trend');
      setData(mockData.sixMonthTrend);
      return;
      
      // TODO: Uncomment when API is ready
      // const userEmail = localStorage.getItem('user_email') || '';
      // if (userEmail === 'saraspr1899@gmail.com') {
      //   setData(mockData.sixMonthTrend);
      //   return;
      // }
      // 
      // const r=await apiFetch("/api/user/usage?range=6m");
      // if(!r.ok) throw new Error();
      // setData(await r.json());
    }catch{ setErr("عدم دریافت آمار شش ماه اخیر"); }
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
