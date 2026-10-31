import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Download, Printer, Search } from 'lucide-react';

interface Payslip {
  name: string;
  employee: string;
  employee_name: string;
  payroll_period: string;
  gross_salary: number;
  cnss_employee: number;
  cnas_employee: number;
  irg: number;
  net_salary: number;
  cnss_employer: number;
  cnas_employer: number;
  total_employer_cost: number;
  days_worked: number;
  overtime_hours: number;
  status: string;
}

export default function PayslipView() {
  const [payslips, setPayslips] = useState<Payslip[]>([]);
  const [periodFilter, setPeriodFilter] = useState('');
  const [selectedPayslip, setSelectedPayslip] = useState<Payslip | null>(null);

  useEffect(() => {
    setPayslips([
      { name: 'SALARY-001', employee: 'EMP-001', employee_name: 'Ahmed Benali', payroll_period: '2024-11', gross_salary: 45000, cnss_employee: 4050, cnas_employee: 225, irg: 3200, net_salary: 37525, cnss_employer: 11700, cnas_employer: 675, total_employer_cost: 57375, days_worked: 26, overtime_hours: 8, status: 'Payé' },
      { name: 'SALARY-002', employee: 'EMP-002', employee_name: 'Fatima Zahra', payroll_period: '2024-11', gross_salary: 55000, cnss_employee: 4950, cnas_employee: 275, irg: 4500, net_salary: 45275, cnss_employer: 14300, cnas_employer: 825, total_employer_cost: 70125, days_worked: 26, overtime_hours: 12, status: 'Payé' },
    ]);
  }, []);

  const filtered = payslips.filter(p => !periodFilter || p.payroll_period === periodFilter);
  const periods = [...new Set(payslips.map(p => p.payroll_period))].sort().reverse();

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Bulletins de Paie</h1>
        <div className="flex items-center gap-4">
          <Select value={periodFilter} onValueChange={setPeriodFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Période" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">Toutes</SelectItem>
              {periods.map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Référence</TableHead>
                <TableHead>Employé</TableHead>
                <TableHead>Période</TableHead>
                <TableHead>Brut</TableHead>
                <TableHead>CNSS</TableHead>
                <TableHead>CNAS</TableHead>
                <TableHead>IRG</TableHead>
                <TableHead>Net</TableHead>
                <TableHead>Coût employeur</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((p) => (
                <TableRow key={p.name}>
                  <TableCell className="font-mono">{p.name}</TableCell>
                  <TableCell>{p.employee_name}</TableCell>
                  <TableCell>{p.payroll_period}</TableCell>
                  <TableCell>{p.gross_salary.toLocaleString()} DA</TableCell>
                  <TableCell>{p.cnss_employee.toLocaleString()} DA</TableCell>
                  <TableCell>{p.cnas_employee.toLocaleString()} DA</TableCell>
                  <TableCell>{p.irg.toLocaleString()} DA</TableCell>
                  <TableCell className="font-bold text-green-600">{p.net_salary.toLocaleString()} DA</TableCell>
                  <TableCell>{p.total_employer_cost.toLocaleString()} DA</TableCell>
                  <TableCell>
                    <Badge variant={p.status === 'Payé' ? 'default' : 'outline'}>{p.status}</Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" onClick={() => setSelectedPayslip(p)}>
                      Voir détail
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {selectedPayslip && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b flex justify-between items-center">
              <h2 className="text-2xl font-bold">Bulletin de Paie - {selectedPayslip.employee_name}</h2>
              <Button variant="ghost" onClick={() => setSelectedPayslip(null)}>
                <Search className="h-5 w-5" />
              </Button>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-500">Période</p>
                  <p className="font-medium">{selectedPayslip.payroll_period}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Jours travaillés</p>
                  <p className="font-medium">{selectedPayslip.days_worked}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Heures sup</p>
                  <p className="font-medium">{selectedPayslip.overtime_hours}h</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Statut</p>
                  <Badge variant="default">{selectedPayslip.status}</Badge>
                </div>
              </div>

              <h3 className="text-lg font-semibold mb-4 border-t pt-4">Gains</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Rubrique</TableHead>
                    <TableHead className="text-right">Montant</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>Salaire de base</TableCell>
                    <TableCell className="text-right">{selectedPayslip.gross_salary.toLocaleString()} DA</TableCell>
                  </TableRow>
                </TableBody>
              </Table>

              <h3 className="text-lg font-semibold mb-4 border-t pt-4">Retenues Salariales</h3>
              <Table>
                <TableBody>
                  <TableRow>
                    <TableCell>CNSS Salarial (9%)</TableCell>
                    <TableCell className="text-right text-red-600">-{selectedPayslip.cnss_employee.toLocaleString()} DA</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>CNAS Salarial (0.5%)</TableCell>
                    <TableCell className="text-right text-red-600">-{selectedPayslip.cnas_employee.toLocaleString()} DA</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>IRG</TableCell>
                    <TableCell className="text-right text-red-600">-{selectedPayslip.irg.toLocaleString()} DA</TableCell>
                  </TableRow>
                </TableBody>
              </Table>

              <h3 className="text-lg font-semibold mb-4 border-t pt-4">Cotisations Patronales</h3>
              <Table>
                <TableBody>
                  <TableRow>
                    <TableCell>CNSS Patronal (26%)</TableCell>
                    <TableCell className="text-right text-blue-600">{selectedPayslip.cnss_employer.toLocaleString()} DA</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>CNAS Patronal (1.5%)</TableCell>
                    <TableCell className="text-right text-blue-600">{selectedPayslip.cnas_employer.toLocaleString()} DA</TableCell>
                  </TableRow>
                </TableBody>
              </Table>

              <div className="mt-6 p-4 bg-green-50 rounded-lg flex justify-between items-center">
                <span className="text-lg font-semibold">Salaire Net à Payer</span>
                <span className="text-2xl font-bold text-green-600">{selectedPayslip.net_salary.toLocaleString()} DA</span>
              </div>
              <div className="mt-2 p-4 bg-blue-50 rounded-lg flex justify-between items-center">
                <span className="text-lg font-semibold">Coût Total Employeur</span>
                <span className="text-2xl font-bold text-blue-600">{selectedPayslip.total_employer_cost.toLocaleString()} DA</span>
              </div>
            </div>
            <div className="p-6 border-t flex justify-end gap-2">
              <Button variant="outline" className="gap-2">
                <Download className="h-4 w-4" />
                PDF
              </Button>
              <Button variant="outline" className="gap-2">
                <Printer className="h-4 w-4" />
                Imprimer
              </Button>
              <Button onClick={() => setSelectedPayslip(null)}>Fermer</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}