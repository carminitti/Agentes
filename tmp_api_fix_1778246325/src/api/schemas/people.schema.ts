import { z } from 'zod';

export const peopleSchema = z.object({
  name: z.string(),
  height: z.string(),
  mass: z.string(),
  birth_year: z.string(),
  gender: z.string(),
  films: z.array(z.string()),
  url: z.string(),
});

export type People = z.infer<typeof peopleSchema>;
