import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Calendar, AlertTriangle, CheckCircle, Upload, Download, Filter } from 'lucide-react';

interface AttendanceRecord {
  name: string;
  employee: string;
  employee_name: string;
  department: string;
  attendance_date: string;
  shift: string;
  check_in: string;
  check_out: string;
  working_hours: number;
  overtime_hours: number;
  late_minutes: number;
  status: string;
  is_anomaly: boolean;
  anomaly_type: string;
}

export default function AttendanceLog() {
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [dateFilter, setDateFilter] = useState('');
  const [showAnomaliesOnly, setShowAnomaliesOnly] = useState(false);

  useEffect(() => {
    // Mock data
    setRecords([
      { name: 'ATT-001', employee: 'EMP-001', employee_name: 'Ahmed Benali', department: 'Réception', attendance_date: '2024-11-15', shift: 'Matin', check_in: '08:05', check_out: '17:10', working_hours: 8.08, overtime_hours: 0, late_minutes: 5, status: 'Retard', is_anomaly: true, anomaly_type: 'Retard' },
      { name: 'ATT-002', employee: 'EMP-002', employee_name: 'Fatima Zahra', department: 'Housekeeping', attendance_date: '2024-11-15', shift: 'Matin', check_in: '07:55', check_out: '16:05', working_hours: 8.17, overtime_hours: 0.17, late_minutes: 0, status: 'Présent', is_anomaly: false, anomaly_type: '' },
      { name: 'ATT-003', employee: 'EMP-003', employee_name: 'Mohamed Amine', department: 'Restauration', attendance_date: '2024-11-15', shift: 'Soir', check_in: '14:00', check_out: '23:30', working_hours: 9.5, overtime_hours: 1.5, late_minutes: 0, status: 'Présent', is_anomaly: false, anomaly_type: '' },
      { name: 'ATT-004', employee: 'EMP-004', employee_name: 'Samira Khelifa', department: 'Maintenance', attendance_date: '2024-11-15', shift: 'Matin', check_in: '', check_out: '', working_hours: 0, overtime_hours: 0, late_minutes: 0, status: 'Absent', is_anomaly: true, anomaly_type: 'Absence non justifiée' },
    ]);
  }, []);

  const filtered = records.filter(r => {
    const matchesDate = !dateFilter || r.attendance_date === dateFilter;
    const matchesAnomaly = !showAnomaliesOnly || r.is_anomaly;
    return matchesDate && matchesAnomaly;
  });

  const anomalyCount = records.filter(r => r.is_anomaly).length;

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Journal de Pointage</h1>
        <div className="flex items-center gap-4">
          <Badge variant={anomalyCount > 0 ? 'destructive' : 'default'} className="gap-2">
            <AlertTriangle className="h-3 w-3" />
            {anomalyCount} anomalies
          </Badge>
          <Button variant="outline" className="gap-2">
            <Upload className="h-4 w-4" />
            Importer
          </Button>
          <Button variant="outline" className="gap-2">
            <Download className="h-4 w-4" />
            Exporter
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <Input
              type="date"
              value={dateFilter}
              onChange={e => setDateFilter(e.target.value)}
              className="w-[200px]"
            />
            <Button variant="outline" onClick={() => setShowAnomaliesOnly(!showAnomaliesOnly)}>
              <Filter className="h-4 w-4 mr-2" />
              {showAnomaliesOnly ? 'Toutes' : 'Anomalies uniquement'}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employé</TableHead>
                <TableHead>Département</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Quart</TableHead>
                <TableHead>Arrivée</TableHead>
                <TableHead>Départ</TableHead>
                <TableHead>Heures</TableHead>
                <TableHead>Heures sup</TableHead>
                <TableHead>Retard</TableHead>
                <TableHead>Statut</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((rec) => (
                <TableRow key={rec.name} className={rec.is_anomaly ? 'bg-red-50' : ''}>
                  <TableCell>{rec.employee_name}</TableCell>
                  <TableCell>{rec.department}</TableCell>
                  <TableCell>{rec.attendance_date}</TableCell>
                  <TableCell><Badge variant="outline">{rec.shift}</Badge></TableCell>
                  <TableCell>{rec.check_in || '—'}</TableCell>
                  <TableCell>{rec.check_out || '—'}</TableCell>
                  <TableCell>{rec.working_hours.toFixed(2)}h</TableCell>
                  <TableCell className={rec.overtime_hours > 0 ? 'text-orange-600 font-medium' : ''}>
                    {rec.overtime_hours.toFixed(2)}h
                  </TableCell>
                  <TableCell className={rec.late_minutes > 0 ? 'text-red-600 font-medium' : ''}>
                    {rec.late_minutes > 0 ? `${rec.late_minutes}min` : '—'}
                  </TableCell>
                  <TableCell>
                    {rec.is_anomaly ? (
                      <Badge variant="destructive" className="gap-1">
                        <AlertTriangle className="h-3 w-3" />
                        {rec.anomaly_type}
                      </Badge>
                    ) : (
                      <Badge variant="default">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        {rec.status}
                      </Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {showAnomaliesOnly && filtered.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <AlertTriangle className="h-12 w-12 mx-auto text-gray-300" />
            <p className="mt-4 text-gray-500">Aucune anomalie pour cette date</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}