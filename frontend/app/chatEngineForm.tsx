"use client";

import React, { useState } from 'react';
import axios, { AxiosError } from 'axios';
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useRouter } from 'next/navigation'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from './components/ui/card';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './components/ui/select';

import { Input } from './components/ui/input';
import { Button } from './components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./components/ui/form";

const formSchema = z.object({
  model: z.string().min(1, { message: "Model is required" }),
  llm_temperature: z.number().min(0).max(1),
  embedding_model: z.string().min(1, { message: "Embedding model is required" }),
  web_url: z.string().optional(),
  file: z.any().optional()
});

type FormSchema = z.infer<typeof formSchema>;

function ChatEngineForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const form = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      model: "",
      llm_temperature: 0.7,
      embedding_model: "",
      web_url: "",
      file: null
    },
  });

  const onSubmit = async (values: FormSchema) => {
    setIsLoading(true);
    const webUrlArray = values.web_url ? values.web_url.split(',').map(url => url.trim()).filter(url => url !== '') : [];

    const jsonData = {
      model: values.model,
      llm_temperature: values.llm_temperature,
      embedding_model: values.embedding_model,
      web_url: webUrlArray.length > 0 ? webUrlArray : undefined
    };

    try {
      const response = await axios.post('http://localhost:8000/chat-engine-settings', jsonData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Response:', response.data);
      if (response.status === 200) {
        router.push("/chat")
      }
    } catch (err) {
      const error = err as Error | AxiosError;
      console.error('Error:', axios.isAxiosError(error) ? error.response?.data : error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center">
      <Card className="w-[380px]">
        <CardHeader>
          <CardTitle>Chat Engine Builder</CardTitle>
          <CardDescription>Deploy your own custom chat engines in one-click.</CardDescription>
        </CardHeader>

        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="model"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Model</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a model" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="gpt-4">gpt-4</SelectItem>
                        <SelectItem value="gpt-4-32k">gpt-4-32k</SelectItem>
                        <SelectItem value="gpt-4-1106-preview">gpt-4-1106-preview</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="llm_temperature"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Temperature</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        step="0.1"
                        min="0"
                        max="1"
                        {...field}
                        onChange={e => field.onChange(parseFloat(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="embedding_model"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Embedding Model</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select an embedding model" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="text-embedding-3-large">text-embedding-3-large</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="web_url"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Web URLs (optional, comma-separated)</FormLabel>
                    <FormControl>
                      <Input placeholder="https://ui.shadcn.com, https://x.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Loading..." : "Deploy"}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}

export default ChatEngineForm;