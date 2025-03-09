import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const data = [
  { name: 'Jan', value: 30 },
  { name: 'Feb', value: 50 },
  { name: 'Mar', value: 40 },
  { name: 'Apr', value: 70 },
  { name: 'May', value: 60 },
  { name: 'Jun', value: 80 },
];

const LineGraph = () => {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#4F46E5" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default LineGraph;
