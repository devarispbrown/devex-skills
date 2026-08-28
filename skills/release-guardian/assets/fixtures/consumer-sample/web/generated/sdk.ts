// Fixture: generated SDK (directory marker 'generated').
export async function listProjects(limit?: number): Promise<Project[]> {
  const res = await fetch(`/v1/projects?limit=${limit ?? 50}`);
  const body = await res.json();
  return body.projects;
}
