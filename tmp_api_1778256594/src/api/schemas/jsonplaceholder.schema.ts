import { z } from 'zod';

export const postSchema = z.object({
  id: z.number(),
  userId: z.number(),
  title: z.string(),
  body: z.string(),
});

export const userSchema = z.object({
  id: z.number(),
  name: z.string(),
  username: z.string(),
  email: z.string().email(),
  address: z.object({
    street: z.string(),
    city: z.string(),
    zipcode: z.string(),
  }),
  company: z.object({
    name: z.string(),
  }),
});

export const todoSchema = z.object({
  id: z.number(),
  userId: z.number(),
  title: z.string(),
  completed: z.boolean(),
});

export type Post = z.infer<typeof postSchema>;
export type User = z.infer<typeof userSchema>;
export type Todo = z.infer<typeof todoSchema>;
