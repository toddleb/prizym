// pages/api/candidates.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const rawProfiles = await prisma.userStarsynProfile.findMany();
    console.log('📊 rawProfiles from DB:', rawProfiles);

    const candidates = rawProfiles.map(row => {
      const profile = row.starsyn_profile;
      return {
        id: profile.candidateId,
        name: profile.userName,
        primaryView: profile.primaryType?.name ?? 'Unknown',
        primaryColor: profile.primaryType?.color ?? '#cccccc',
        secondaryInfluences: profile.secondaryInfluences?.map((s: any) => s.name) ?? [],
        skills: profile.skillCategories?.flatMap((sc: any) =>
          Array.isArray(sc.skills) ? sc.skills.map((sk: any) => sk.name) : []
        ) ?? [],
        matchScore: profile.skillCategories?.reduce((acc: number, sc: any) => acc + (sc.score || 0), 0) ?? 0,
        intent: 'medium', // Placeholder
        lastActivity: '3d ago', // Placeholder
        futureGoals: [], // Placeholder
        isRevealed: false
      };
    });

    res.status(200).json({ candidates });
  } catch (error) {
    console.error('[API ERROR] /api/candidates', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

