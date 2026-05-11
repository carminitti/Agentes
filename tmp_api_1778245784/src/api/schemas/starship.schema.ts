import { z } from 'zod';

export const starshipSchema = z.object({
  name: z.string(),
  model: z.string(),
  manufacturer: z.string(),
  url: z.string(),
});

export type Starship = z.infer<typeof starshipSchema>;
