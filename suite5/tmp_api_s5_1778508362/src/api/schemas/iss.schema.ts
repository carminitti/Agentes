import { z } from 'zod';
export const issSchema = z.object({
  message: z.string(),
  timestamp: z.number(),
  iss_position: z.object({
    latitude: z.string().or(z.number()),
    longitude: z.string().or(z.number()),
  }),
});
export type ISSPosition = z.infer<typeof issSchema>;
