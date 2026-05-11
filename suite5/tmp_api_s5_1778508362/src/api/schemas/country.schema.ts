import { z } from 'zod';
export const countrySchema = z.object({
  name: z.object({ common: z.string() }),
  capital: z.array(z.string()).optional(),
  population: z.number(),
  currencies: z.record(z.any()).optional(),
});
export type Country = z.infer<typeof countrySchema>;
