import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Filter, Download } from 'lucide-react';

interface Employee {
  name: string;
  employee_id: string;
  employee_name: string;
  department: string;
  designation: string;
  employment_type: string;
  status: string;
  date_of_joining: string;
}

export default function EmployeeList() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    // TODO: Fetch from API
    // fetch('/api/method/ziri_hr.api.employee_api.get_employees')
    setEmployees([
      { name: 'EMP-001', employee_id: 'EMP-001', employee_name: 'Ahmed Benali', department: 'Réception', designation: 'Réceptionniste', employment_type: 'CDI', status: 'Actif', date_of_joining: '2023-01-15' },
      { name: 'EMP-002', employee_id: 'EMP-002', employee_name: 'Fatima Zahra', department: 'Housekeeping', designation: 'Gouvernante', employment_type: 'CDI', status: 'Actif', date_of_joining: '2022-03-20' },
      { name: 'EMP-003', employee_id: 'EMP-003', employee_name: 'Mohamed Amine', department: 'Restauration', designation: 'Serveur', employment_type: 'CDD', status: 'Actif', date_of_joining: '2024-06-01' },
      { name: 'EMP-004', employee_id: 'EMP-004', employee_name: 'Samira Khelifa', department: 'Maintenance', designation: 'Technicien', employment_type: 'CDI', status: 'En congé', date_of_joining: '2021-11-10' },
    ]);
  }, []);

  const filtered = employees.filter(e => {
    const matchesSearch = e.employee_name.toLowerCase().includes(search.toLowerCase()) ||
                          e.employee_id.toLowerCase().includes(search.toLowerCase());
    const matchesDept = !deptFilter || e.department === deptFilter;
    const matchesStatus = !statusFilter || e.status === statusFilter;
    return matchesSearch && matchesDept && matchesStatus;
  });

  const statusColors: Record<string, string> = {
    'Actif': 'bg-green-100 text-green-800',
    'En congé': 'bg-blue-100 text-blue-800',
    'Suspendu': 'bg-yellow-100 text-yellow-800',
    'Démissionné': 'bg-red-100 text-red-800',
  };

  const departments = ['Réception', 'Housekeeping', 'Restauration', 'Maintenance', 'Administration'];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Gestion du Personnel</h1>
        <Button className="gap-2" onClick={() => {/* open create modal */}}>
          <Plus className="h-4 w-4" />
          Nouvel employé
        </Button>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Rechercher par nom ou matricule..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={deptFilter} onValueChange={setDeptFilter}>
              <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Département" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Tous</SelectItem>
                {departments.map(d => <SelectItem key={d} value={d}>{d}</SelectItem>)}
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Statut" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Tous</SelectItem>
                <SelectItem value="Actif">Actif</SelectItem>
                <SelectItem value="En congé">En congé</SelectItem>
                <SelectItem value="Suspendu">Suspendu</SelectItem>
                <SelectItem value="Démissionné">Démissionné</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" className="gap-2">
              <Download className="h-4 w-4" />
              Exporter
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Matricule</TableHead>
                <TableHead>Nom</TableHead>
                <TableHead>Département</TableHead>
                <TableHead>Poste</TableHead>
                <TableHead>Type contrat</TableHead>
                <TableHead>Entrée</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((emp) => (
                <TableRow key={emp.name}>
                  <TableCell className="font-mono">{emp.employee_id}</TableCell>
                  <TableCell>{emp.employee_name}</TableCell>
                  <TableCell>{emp.department}</TableCell>
                  <TableCell>{emp.designation}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{emp.employment_type}</Badge>
                  </TableCell>
                  <TableCell>{emp.date_of_joining}</TableCell>
                  <TableCell>
                    <Badge className={statusColors[emp.status] || 'bg-gray-100 text-gray-800'}>
                      {emp.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" className="gap-1">
                      Voir
                    </Button>
                    <Button variant="ghost" size="sm" className="gap-1">
                      Modifier
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}