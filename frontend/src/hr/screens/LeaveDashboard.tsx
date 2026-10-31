import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Calendar, Clock, CheckCircle, XCircle, AlertCircle, Plus } from 'lucide-react';

interface LeaveRequest {
  name: string;
  employee: string;
  employee_name: string;
  leave_type: string;
  from_date: string;
  to_date: string;
  total_days: number;
  status: string;
  reason: string;
}

export default function LeaveDashboard() {
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // Mock data
    setRequests([
      { name: 'LEA-001', employee: 'EMP-001', employee_name: 'Ahmed Benali', leave_type: 'Congés Annuels', from_date: '2024-12-20', to_date: '2024-12-27', total_days: 6, status: 'Approuvé Manager', reason: 'Vacances famille' },
      { name: 'LEA-002', employee: 'EMP-002', employee_name: 'Fatima Zahra', leave_type: 'Maladie', from_date: '2024-11-15', to_date: '2024-11-17', total_days: 3, status: 'Approuvé', reason: 'Grippe' },
      { name: 'LEA-003', employee: 'EMP-003', employee_name: 'Mohamed Amine', leave_type: 'Congés Annuels', from_date: '2024-12-25', to_date: '2025-01-05', total_days: 10, status: 'Soumis', reason: 'Voyage' },
      { name: 'LEA-004', employee: 'EMP-004', employee_name: 'Samira Khelifa', leave_type: 'Maternité', from_date: '2025-01-15', to_date: '2025-04-15', total_days: 90, status: 'Approuvé RH', reason: 'Congé maternité' },
    ]);
  }, []);

  const statusConfig: Record<string, { icon: React.ComponentType<{className?: string}>; color: string; label: string }> = {
    'Brouillon': { icon: AlertCircle, color: 'text-gray-600', label: 'Brouillon' },
    'Soumis': { icon: Clock, color: 'text-blue-600', label: 'Soumis' },
    'Approuvé Manager': { icon: AlertCircle, color: 'text-orange-600', label: 'À valider RH' },
    'Approuvé RH': { icon: CheckCircle, color: 'text-purple-600', label: 'Approuvé RH' },
    'Approuvé': { icon: CheckCircle, color: 'text-green-600', label: 'Approuvé' },
    'Rejeté': { icon: XCircle, color: 'text-red-600', label: 'Rejeté' },
    'Annulé': { icon: XCircle, color: 'text-gray-600', label: 'Annulé' },
  };

  const filtered = requests.filter(r => filter === 'all' || r.status === filter);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Gestion des Congés</h1>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Nouvelle demande
        </Button>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-2">
            <Button variant={filter === 'all' ? 'default' : 'outline'} onClick={() => setFilter('all')}>Tous</Button>
            <Button variant={filter === 'Soumis' ? 'default' : 'outline'} onClick={() => setFilter('Soumis')}>En attente</Button>
            <Button variant={filter === 'Approuvé Manager' ? 'default' : 'outline'} onClick={() => setFilter('Approuvé Manager')}>À valider</Button>
            <Button variant={filter === 'Approuvé' ? 'default' : 'outline'} onClick={() => setFilter('Approuvé')}>Approuvés</Button>
            <Button variant={filter === 'Rejeté' ? 'default' : 'outline'} onClick={() => setFilter('Rejeté')}>Rejetés</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Référence</TableHead>
                <TableHead>Employé</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Période</TableHead>
                <TableHead>Jours</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead>Motif</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((req) => {
                const cfg = statusConfig[req.status] || { icon: AlertCircle, color: 'text-gray-600', label: req.status };
                return (
                  <TableRow key={req.name}>
                    <TableCell className="font-mono">{req.name}</TableCell>
                    <TableCell>{req.employee_name}</TableCell>
                    <TableCell><Badge variant="outline">{req.leave_type}</Badge></TableCell>
                    <TableCell>{req.from_date} → {req.to_date}</TableCell>
                    <TableCell>{req.total_days}</TableCell>
                    <TableCell>
                      <Badge className={`flex items-center gap-1 ${cfg.color}`}>
                        <cfg.icon className="h-3 w-3" />
                        {cfg.label}
                      </Badge>
                    </TableCell>
                    <TableCell className="max-w-xs truncate">{req.reason}</TableCell>
                    <TableCell className="text-right">
                      {req.status === 'Soumis' && (
                        <Button variant="ghost" size="sm" onClick={() => {/* approve */}}>Valider</Button>
                      )}
                      {req.status === 'Approuvé Manager' && (
                        <Button variant="default" size="sm" onClick={() => {/* hr approve */}}>Valider RH</Button>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}