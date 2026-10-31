import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Users, Calendar, Clock, TrendingUp, AlertTriangle } from 'lucide-react';

interface HRSummary {
  totalEmployees: number;
  activeEmployees: number;
  newHires: number;
  departures: number;
  pendingLeaves: number;
  attendanceRate: number;
  overtimeHours: number;
  payrollCost: number;
}

export default function HRDashboard() {
  const [summary, setSummary] = useState<HRSummary>({
    totalEmployees: 0,
    activeEmployees: 0,
    newHires: 0,
    departures: 0,
    pendingLeaves: 0,
    attendanceRate: 0,
    overtimeHours: 0,
    payrollCost: 0
  });

  useEffect(() => {
    // TODO: Fetch from API
    // fetch('/api/method/ziri_hr.api.dashboard.get_summary')
    //   .then(res => res.json())
    //   .then(data => setSummary(data))
    
    // Mock data for now
    setSummary({
      totalEmployees: 145,
      activeEmployees: 138,
      newHires: 8,
      departures: 3,
      pendingLeaves: 12,
      attendanceRate: 94.5,
      overtimeHours: 256,
      payrollCost: 2845000
    });
  }, []);

  const stats = [
    { title: 'Effectif Total', value: summary.totalEmployees, icon: Users, color: 'text-blue-600' },
    { title: 'Actifs', value: summary.activeEmployees, icon: TrendingUp, color: 'text-green-600' },
    { title: 'Nouvelles embauches', value: summary.newHires, icon: Users, color: 'text-purple-600' },
    { title: 'Congés en attente', value: summary.pendingLeaves, icon: Calendar, color: 'text-orange-600' },
    { title: 'Taux présence', value: `${summary.attendanceRate}%`, icon: Clock, color: 'text-indigo-600' },
    { title: 'Heures sup', value: summary.overtimeHours, icon: AlertTriangle, color: 'text-red-600' },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tableau de bord RH</h1>
        <Badge variant="outline">Algérie - DZD</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stats.map((stat, idx) => (
          <Card key={idx}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Effectifs par département</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {[
                { dept: 'Réception', count: 28 },
                { dept: 'Housekeeping', count: 42 },
                { dept: 'Restauration', count: 35 },
                { dept: 'Maintenance', count: 12 },
                { dept: 'Administration', count: 21 },
              ].map((d, idx) => (
                <div key={idx} className="flex items-center justify-between">
                  <span>{d.dept}</span>
                  <Badge variant="secondary">{d.count}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Alertes RH</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-amber-600">
                <AlertTriangle className="h-4 w-4" />
                <span>3 contrats expirent ce mois</span>
              </div>
              <div className="flex items-center gap-2 text-blue-600">
                <Calendar className="h-4 w-4" />
                <span>12 demandes congés en attente</span>
              </div>
              <div className="flex items-center gap-2 text-red-600">
                <Clock className="h-4 w-4" />
                <span>5 anomalies pointage hier</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}