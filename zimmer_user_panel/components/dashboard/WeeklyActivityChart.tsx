"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card, Skeleton } from "@/components/Skeleton";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";
import { mockData } from "@/lib/mockApi";

type Row = { day:string; tokens:number; sessions:number };

export default function WeeklyActivityChart(){
  const [data,setData]=useState<Row[]|null>(null);
  const [err,setErr]=useState<string|null>(null);
  useEffect(()=>{(async()=>{
    try{
      // Always use mock data for now since API endpoints are not ready
      console.log('Using mock data for weekly usage');
      setData(mockData.weeklyUsage);
      return;
      
      // TODO: Uncomment when API is ready
      // const userEmail = localStorage.getItem('user_email') || '';
      // if (userEmail === 'saraspr1899@gmail.com') {
      //   setData(mockData.weeklyUsage);
      //   return;
      // }
      // 
      // const r=await apiFetch("/api/user/usage?range=7d");
      // if(!r.ok) throw new Error();
      // setData(await r.json());
    }catch{ setErr("عدم دریافت فعالیت هفتگی"); }
  })()},[]);
  return (
    <Card className="col-span-12 lg:col-span-7">
      <div className="font-semibold mb-3">فعالیت هفتگی</div>
      {!data && !err && <Skeleton className="h-64" />}
      {err && <div className="text-sm text-red-600">{err}</div>}
      {data && (
        <motion.div initial={{opacity:0}} animate={{opacity:1}}>
          <div style={{width:"100%", height:260}}>
            <ResponsiveContainer>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="tokens" fill="#8B5CF6" />
                <Bar dataKey="sessions" fill="#10B981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}
    </Card>
  );
}
