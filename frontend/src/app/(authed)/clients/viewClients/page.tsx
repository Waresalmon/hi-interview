"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Loader, Title, Text } from "@mantine/core";
import { useApi } from "@/api/context";
import { Client } from "@/types/clients";

export default function ClientDetailPage() {
  const params = useParams();
  const clientId = params.client_id;
  const api = useApi();

  const [client, setClient] = useState<Client | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.clients.getClientById(clientId)
      .then(setClient)
      .finally(() => setLoading(false));
  }, [api, clientId]);

  if (loading) return <Loader />;

  if (!client) return <Text>Client not found</Text>;

  return (
    <div>
      <Title order={2}>{client.first_name} {client.last_name}</Title>
      <Text>Email: {client.email}</Text>
      <Text>Assigned Advisor: {client.assigned_user_id || "None"}</Text>
      <Text>Created At: {new Date(client.created_at).toLocaleString()}</Text>
      <Text>Updated At: {new Date(client.updated_at).toLocaleString()}</Text>
    </div>
  );
}