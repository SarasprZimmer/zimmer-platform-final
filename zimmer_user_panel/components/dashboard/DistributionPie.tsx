"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card, Skeleton } from "@/components/Skeleton";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";
import { mockData } from "@/lib/mockApi";

type Slice = { name:string; value:number; color?:string };

export default function DistributionPie(){
  const [data,setData]=useState<Slice[]|null>(null);
  const [err,setErr]=useState<string|null>(null);
  useEffect(()=>{(async()=>{
    try{
      // Always use mock data for now since API endpoints are not ready
      console.log('Using mock data for distribution');
      setData(mockData.distribution);
      return;
      
      // TODO: Uncomment when API is ready
      // const userEmail = localStorage.getItem('user_email') || '';
      // if (userEmail === 'saraspr1899@gmail.com') {
      //   setData(mockData.distribution);
      //   return;
      // }
      // 
      // const r=await apiFetch("/api/user/usage/distribution");
      // if(!r.ok) throw new Error();
      // setData(await r.json());
    }catch{ setErr("عدم دریافت آمار اتوماسیون‌ها"); }
  })()},[]);
  return (
    <Card className="col-span-12 lg:col-span-5">
      <div className="font-semibold mb-3">آمار اتوماسیون‌ها</div>
      {!data && !err && <Skeleton className="h-64" />}
      {err && <div className="text-sm text-red-600">{err}</div>}
      {data && (
        <motion.div initial={{scale:0.97, opacity:0}} animate={{scale:1, opacity:1}}>
          <div style={{width:"100%", height:260}}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={data} dataKey="value" nameKey="name" outerRadius={100}>
                  {data.map((entry,i)=>(<Cell key={i} fill={entry.color || `hsl(${i * 60}, 70%, 50%)`} />))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}
    </Card>
  );
}
