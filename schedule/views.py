from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Day, Seat, Worker

class SeatListView(View):
    def get(self, request):
        days = Day.objects.prefetch_related('seats__worker').all().order_by('id')
        user_worker = request.worker

        
        return render(request, 'schedule/seat_list.html', {
            'days': days,
            'user_worker': user_worker
        })


    def post(self, request):
        seat_id = request.POST.get('seat')
        action = request.POST.get('action')  # NUEVO
        
        try:
            seat = Seat.objects.get(pk=seat_id)
            worker = request.worker
            
            # --- ACCIÓN LIBERAR ---
            if action == "free":
                if seat.worker == worker:
                    seat.worker = None
                    seat.save()

                    # Enviar actualización por WebSocket
                    from channels.layers import get_channel_layer
                    from asgiref.sync import async_to_sync
                    
                    layer = get_channel_layer()
                    async_to_sync(layer.group_send)(
                        "schedule",
                        {
                            "type": "seat_update",
                            "data": {
                                "seat_id": seat.id,
                                "worker": None,
                                "day": seat.day.get_day_of_week_display(),
                                "position": seat.position
                            }
                        }
                    )
                    
                    messages.success(request, "Has liberado tu turno.")
                else:
                    messages.error(request, "No puedes liberar un turno que no te pertenece.")
                
                return redirect('schedule:seat_list')
            
            # --- ACCIÓN ASIGNAR ---
            if action == "assign":
                if seat.worker is not None:
                    messages.error(request, "Este asiento ya está ocupado.")
                    return redirect('schedule:seat_list')

                seat.worker = worker
                seat.save()

                # Notificar por WebSocket
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                
                layer = get_channel_layer()
                async_to_sync(layer.group_send)(
                    "schedule",
                    {
                        "type": "seat_update",
                        "data": {
                            "seat_id": seat.id,
                            "worker": worker.name,
                            "day": seat.day.get_day_of_week_display(),
                            "position": seat.position
                        }
                    }
                )

                messages.success(request, "Te asignaste correctamente.")
        
        except Seat.DoesNotExist:
            messages.error(request, "Asiento no válido.")

        return redirect('schedule:seat_list')


class WorkerListView(ListView):
    model = Worker
    template_name = 'schedule/worker_list.html'
    context_object_name = 'workers'

class WorkerCreateView(CreateView):
    model = Worker
    template_name = 'schedule/worker_form.html'
    fields = ['name']
    success_url = reverse_lazy('schedule:worker_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Trabajador creado exitosamente')
        return super().form_valid(form)

class WorkerUpdateView(UpdateView):
    model = Worker
    template_name = 'schedule/worker_form.html'
    fields = ['name']
    success_url = reverse_lazy('schedule:worker_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Trabajador actualizado exitosamente')
        return super().form_valid(form)

class WorkerDeleteView(DeleteView):
    model = Worker
    template_name = 'schedule/worker_confirm_delete.html'
    success_url = reverse_lazy('schedule:worker_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Trabajador eliminado exitosamente')
        return super().delete(request, *args, **kwargs)

@require_POST
def reset_assignments(request):
    Seat.objects.all().update(worker=None)
    messages.success(request, "Todas las asignaciones han sido reiniciadas correctamente.")
    return redirect('schedule:seat_list')