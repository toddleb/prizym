import { PrismaClient } from '@prisma/client';
import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import path from 'path';
import { mkdirSync, existsSync } from 'fs';

const prisma = new PrismaClient();

export async function POST(req: NextRequest) {
  const form = await req.formData();

  const name = form.get('name') as string;
  const email = form.get('email') as string;
  const org = form.get('org') as string;
  const consent = form.get('consent') === 'on';
  const file = form.get('file') as File;

  if (!file || !file.name) {
    return NextResponse.json({ success: false, error: 'No file uploaded' }, { status: 400 });
  }

  // Prepare upload directory
  const uploadDir = path.join(process.cwd(), 'public/uploads');
  if (!existsSync(uploadDir)) {
    mkdirSync(uploadDir, { recursive: true });
  }

  // Save file
  const buffer = Buffer.from(await file.arrayBuffer());
  const timestamp = Date.now();
  const safeFilename = `${timestamp}-${file.name.replace(/[^a-zA-Z0-9.\\-_]/g, '')}`;
  const filepath = path.join(uploadDir, safeFilename);
  await writeFile(filepath, buffer);

  // Save form data to DB
  const submission = await prisma.submission.create({
    data: {
      name,
      email,
      org,
      consent,
      filename: safeFilename,
    },
  });

  return NextResponse.json({ success: true, submission });
}
