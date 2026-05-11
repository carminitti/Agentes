import { z } from 'zod';

export const userSchema = z.object({
  id: z.number(),
  name: z.string(),
  username: z.string(),
  email: z.string(),
  address: z.object({
    street: z.string(),
    suite: z.string(),
    city: z.string(),
    zipcode: z.string(),
    geo: z.object({ lat: z.string(), lng: z.string() }),
  }).optional(),
  phone: z.string().optional(),
  website: z.string().optional(),
  company: z.object({
    name: z.string(),
    catchPhrase: z.string(),
    bs: z.string(),
  }).optional(),
});

export const postSchema = z.object({
  id: z.number(),
  userId: z.number(),
  title: z.string().min(1),
  body: z.string().min(1),
});

export const commentSchema = z.object({
  id: z.number(),
  postId: z.number(),
  name: z.string(),
  email: z.string().email(),
  body: z.string(),
});

export const todoSchema = z.object({
  id: z.number(),
  userId: z.number(),
  title: z.string().min(1),
  completed: z.boolean(),
});

export type User = z.infer<typeof userSchema>;
export type Post = z.infer<typeof postSchema>;
export type Comment = z.infer<typeof commentSchema>;
export type Todo = z.infer<typeof todoSchema>;
