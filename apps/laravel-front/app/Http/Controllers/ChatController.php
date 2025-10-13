<?php
declare(strict_types=1);

namespace App\Http\Controllers;

use Illuminate\View\View;

final class ChatController extends Controller
{
    /**
     * Affiche l’UI du chat (Phase 1, stub)
     */
    public function index(): View
    {
        // Phase 1 : on ne passe aucune donnée métier,
        // juste un titre ou une config minimale
        return view('chat.index', [
            'title' => 'Huginn • Chat (Phase 1 – UI only)'
        ]);
    }
}
